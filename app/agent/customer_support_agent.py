# app/agent/customer_support_agent.py


from app.agent.supervisor_agent import SupervisorAgent

from app.utils.io_comunications import UserIO #write, read
from app.utils.storage import save_conversation, load_conversations, list_all_orders
from typing import Literal

from app.utils.prompt_loader import load_prompts




REQUIRED_KEYS = ["order_number", "category", "description", "urgency"]
MAX_MSG = 50

class CustomerSupportAgent:
    check_every_n_msg = 3 # After how many msg the suppervisor is going to check the work of the customer agent
    cached_order_logs = None
    def __init__(self, model, mode: Literal["rigid", "natural"] = "rigid", company: str = "ExampleCorp", audio_mode:bool = True, lang: str = "en", verbose:bool = False, read_silence_duration:float= 2.0, read_max_duration:int = 60, read_silence_threshold:int = 5) -> None:
        self.model = model
        self.mode = mode
        self.company = company
        self.audio_mode = audio_mode
        self.verbose = verbose
        self.lang = lang
        self.prompts = load_prompts("customer_support", lang)

        self.conversation = [] # This will contain only the latest notes, al previous ones are removed from the conversation
        self.full_conversation = [] # Contains all the notes
        self.extracted = {}
        self.supervisor = SupervisorAgent(model, REQUIRED_KEYS, lang, verbose)
        self.userIO = UserIO(model, verbose, silence_duration=read_silence_duration, max_duration=read_max_duration,silence_threshold=read_silence_threshold)# Needed for text/audio input/ouputs comunications
        


    def start(self):
        if self.mode == "rigid":
            self._start_rigid()
        elif self.mode == "natural":
            self._start_natural()
        else:
            raise ValueError("Mode must be 'rigid' or 'natural'")

    def _start_rigid(self):
        

        """questions = {
            "order_number": "What is your order number?",
            "category": "What issue are you experiencing (shipping, billing, product)?",
            "description": "Can you briefly describe the issue?",
            "urgency": "How urgent is this? (low, medium, high)",
        }"""
        questions = self.prompts["questions"]

        self.conversation.append({"role": "developer", "content": self.prompts["system_prompt"]}) 

        for key, q in questions.items():
            while True:
                convo_input = {"role": "assistant", "content": q}
                if self.verbose:
                    print("\n")
                self.userIO.write(f"🤖 {q}", audio=self.audio_mode)
                user_input = self.userIO.read("> ", audio=self.audio_mode)

                convo_user = {"role": "user", "content": user_input}
                self.conversation.extend([convo_input, convo_user])

                validate_prompt = self.conversation + [
                    {
                        "role": "developer",
                        "content": self.prompts["validation_instruction"].format(key=key, invalid_response="INVALID") 
                    }
                ]
                result = self.model.chat(validate_prompt)
                
                if self.verbose:
                    print(f"[DEBUG] \n Validate Prompt: {validate_prompt} \n Result: {result}")
                if result.lower() != "invalid":
                    self.extracted[key] = result
                    break
                else:
                    self.userIO.write(self.prompts["invalid_input"], audio=self.audio_mode)

        summary_prompt = self.conversation + [
            {"role": "developer", "content": self.prompts["summary_instruction"]}
        ]
        summary = self.model.chat(summary_prompt)


        # Find Customer frustration
        frustration_prompt = self.conversation + [
            {"role": "developer", "content": self.prompts["customer_frustration"]}
        ]
        frustration_score = self.model.chat(frustration_prompt)
        if self.verbose:
            print(f"[DEBUG] \n Frustration Prompt: {frustration_prompt} \n frustration_score: {frustration_score}")
        try:
            score = int(frustration_score)
            if 0 <= score <= 10:
                frustration_score = score
            else:
                frustration_score = None
        except ValueError:
            frustration_score = None
        if self.verbose:
            print(f"[DEBUG] \n Frustration Prompt: {frustration_prompt} \n frustration_score: {frustration_score}")


        # Save the conversation + the info extracted + summary to json + frustration score
        save_conversation(self.extracted, self.conversation, summary, "natural", frustration_score,  self.lang)

        self.userIO.write(self.prompts["extracted_info"].format(extracted=self.extracted), audio=self.audio_mode)
        self.userIO.write(self.prompts["summary_prefix"].format(summary=summary), audio=self.audio_mode) 

    def _start_natural(self):
        welcome = self.prompts["welcome"].format(company=self.company) 
        if self.verbose:
            print("\n")
        self.userIO.write(f"🤖 {welcome}", audio = self.audio_mode)
        self.full_conversation.append({"role": "system", "content": self.prompts["system_prompt"]}) 
        self.full_conversation.append({"role": "assistant", "content": welcome})

        msgs_count = 1 # count the msg wiht the user

        while not self._all_info_collected() and msgs_count < MAX_MSG: # To prevent infinite conversations
            # remove all past developer comments, this is done to track only the conversation + the last notes
            self.conversation = self.remove_developer_notes() # clean previous developer coments, and add the new ones

            user_input = self.userIO.read("> ", audio=self.audio_mode)
            self.full_conversation.append({"role": "user", "content": user_input})
            self.conversation.append({"role": "user", "content": user_input})


            msg = self.prompts["partial_notes"].format(extracted=self.extracted) 
            self.full_conversation.append({"role": "developer", "content":msg})
            self.conversation.append({"role": "developer", "content":msg}) # Add the notes also to the conversation, so that the extraction have context on the notes


            # Try to extract info
            for key in REQUIRED_KEYS:
                if key in self.extracted:
                    continue
                # We are using the conversation without the history of notes, just the last notes taken
                extract_prompt = self.conversation + [
                    {
                        "role": "developer",
                        "content": self.prompts["validation_instruction"].format(key=key, invalid_response="NONE") 
                    }
                ]
                result = self.model.chat(extract_prompt)

                if self.verbose:
                    print(f"[DEBUG] \n Validate Prompt: {extract_prompt} \n Result: {result}")
                if result.lower() != "none":
                    self.extracted[key] = result

            # Check the information is correct
            if self._all_info_collected() or msgs_count%self.check_every_n_msg==0: # we also check every 'self.check_every_n_msg' msg in case the main agent missed something
                validation = self.supervisor.validate(self.conversation, self.extracted)
                if validation:
                    # Correct we stop
                    self.userIO.write(f"🤖 {self.prompts["thanks_message"]}", audio=self.audio_mode) 
                    break
                else:
                    msg = self.prompts["supervisor_correction"].format(extracted=self.extracted, required_keys=REQUIRED_KEYS)
                    self.full_conversation.append({"role": "developer", "content":msg})
                    self.conversation.append({"role": "developer", "content":msg})


            # Check if previous conversation with this order. if its the case add the previous conversations as a history:
            conv_history = self._check_and_add_history()
            if conv_history: # Only save if there is a history
                self.conversation.insert(1, {"role": "developer", "content":conv_history}) # We dont save it to the full conversation since we dont want to save the history again to the json

            
            # Get assistant reply
            assistant_reply = self.model.chat(self.conversation)
            self.full_conversation.append({"role": "assistant", "content": assistant_reply})
            self.conversation.append({"role": "assistant", "content": assistant_reply})
            self.userIO.write(f"🤖 {assistant_reply}", audio=self.audio_mode)
            if self.verbose:
                print(f"[DEBUG] \n MODEL Prompt: {self.conversation} \n assistant_reply: {assistant_reply}")
                print("\n")
            
            msgs_count+=1# Increase the number of msg with the users
        # End loop

        self.conversation = self.remove_developer_notes() # Remove all the developer notes, since those are auxiliary msg to add context to the model, but not important for the summary
        msg = self.prompts["partial_notes"].format(extracted=self.extracted) 
        self.conversation.append({"role": "developer", "content":msg})
        summary_prompt = self.conversation + [
            {"role": "developer", "content": self.prompts["summary_instruction"]}
        ]
        summary = self.model.chat(summary_prompt)

        # Find Customer frustration
        frustration_prompt = self.conversation + [
            {"role": "assistant", "content": self.prompts["customer_frustration"]}
        ]
        frustration_score = self.model.chat(frustration_prompt)
        if self.verbose:
            print(f"[DEBUG] \n Frustration Prompt: {frustration_prompt} \n frustration_score: {frustration_score}")
        try:
            score = int(frustration_score)
            if 0 <= score <= 10:
                frustration_score = score
            else:
                frustration_score = None
        except ValueError:
            frustration_score = None
        if self.verbose:
            print(f"[DEBUG] \n Frustration Prompt: {frustration_prompt} \n frustration_score: {frustration_score}")


        # Save the conversation + the info extracted + summary to json + frustration score
        save_conversation(self.extracted, self.conversation, summary, "natural", frustration_score,  self.lang)
        
        self.userIO.write(self.prompts["extracted_info"].format(extracted=self.extracted), audio=self.audio_mode)
        self.userIO.write(self.prompts["summary_prefix"].format(summary=summary), audio=self.audio_mode)


    def remove_developer_notes(self):
        filtered_list = [d for d in self.full_conversation if d.get("role") != "developer"]
        return filtered_list

    def _all_info_collected(self):
        return all(k in self.extracted for k in REQUIRED_KEYS)

    def get_summary(self):
        return self.extracted


    def _check_and_add_history(self):
        if "order_number" not in self.extracted:
            return None  # Nothing to do if we don't have an order number yet

        if self.cached_order_logs:
            return self.cached_order_logs  # Already loaded

        order_id = self.extracted["order_number"]

        if order_id in list_all_orders():
            previous_data = load_conversations(order_id)

            msg = self.prompts["history_msg"].format(order_id=order_id) 
            for conv in previous_data:
                timestamp_log = conv.get("timestamp", "")
                conversation_log = conv.get("conversation", "")
                msg += f"\n\n{timestamp_log} -> "
                # Loop through each message in the conversation
                for message in conversation_log:
                    role = message.get("role")
                    content = message.get("content", "")

                    # Skip the system messages
                    if role == "system":
                        continue
                    
                    # Format the conversation based on the role
                    if role == "user":
                        msg += f"\n[USER]: \"{content}\""
                    elif role == "assistant":
                        msg += f"\n[YOU]: \"{content}\""
                    elif role == "developer":
                        msg += f"\n[DEVELOPER]: \"{content}\""


            self.cached_order_logs = msg
            return msg

        return None  # If order_id not found
