# app/agent/supervisor_agent.py

from app.data_validation.data_validation import validate_and_extract
import ast

from app.utils.prompt_loader import load_prompts

class SupervisorAgent:
    def __init__(self, model, required_keys, lang: str = "en", verbose: bool = False):
        self.model = model
        self.required_keys = required_keys
        self.verbose = verbose
        self.lang = lang
        self.prompts = load_prompts("supervisor", lang)

    def _format(self, key: str, **kwargs):
        return self.prompts[key].format(**kwargs)
    
    def validate(self, conversation, extracted):
        if self.verbose:
            print(f"\n\n ----- VALIDATOR -----\n\n ")

        # Initial validation
        prompt = self._format("role_intro", conversation=conversation)
        manager_conv = [{"role": "system", "content": prompt}]

        msg = self._format("notes_check", required_keys=self.required_keys, extracted=extracted)
        manager_conv.append({"role": "user", "content": msg})

        result = self.model.chat(manager_conv)
        if self.verbose:
            print(f"[DEBUG] \n Validator Prompt: {manager_conv} \n Result: {result}\n")

        manager_conv.append({"role": "assistant", "content": result})

        if result.lower() != 'yes':
            # Incorrect information, finding errors and fixing
            # Attempt to fix
            fix_prompt = self.prompts["fix_prompt"]
            manager_conv.append({"role": "user", "content": fix_prompt})
            
            result = self.model.chat(manager_conv)

            if self.verbose:
                print(f"[DEBUG] \n Validator Prompt: {manager_conv} \n Result: {result}\n")

            manager_conv.append({"role": "assistant", "content": result})

            if result.lower() != 'yes':
                # The conversation doest have all the information needed, Ask which categories are incorrect
                # Ask for incorrect fields
                categories_prompt = self._format("which_incorrect", required_keys=self.required_keys)
                manager_conv.append({"role": "user", "content": categories_prompt})
                
                result = self.model.chat(manager_conv)

                if self.verbose:
                    print(f"[DEBUG] \n Validator Prompt: {manager_conv} \n Result: {result}\n")

                manager_conv.append({"role": "assistant", "content": result})

                try:
                    incorrect = ast.literal_eval(result)
                    if not isinstance(incorrect, list):
                        raise ValueError("[DEBUG] The result is not a list.")
                    
                    # Remove the incorrect categories
                    for cat in incorrect:
                        extracted.pop(cat, None)
                except Exception as e:
                    if self.verbose:
                        print("[DEBUG] Error converting to list:", e)
                return False
            else:
                # Fix and update dict
                # Try fixing the notes
                fix_notes_prompt = self._format("fix_notes", required_keys=self.required_keys)
                manager_conv.append({"role": "user", "content": fix_notes_prompt})
                
                result = self.model.chat(manager_conv)

                if self.verbose:
                    print(f"[DEBUG] \n Validator Prompt: {manager_conv} \n Result: {result}\n")

                manager_conv.append({"role": "assistant", "content": result})

                try:
                    updates = ast.literal_eval(result)
                    if not isinstance(updates, dict):
                        raise ValueError("[DEBUG] The result is not a dictionary.")
                    

                    # Update the structured information with the correct information
                    extracted.update(updates)

                except Exception as e:
                    if self.verbose:
                        print("[DEBUG] Error converting to dict:", e)

                pass # There are problems but we fixed it
        else:
            # Information is correct and we end
            pass

        # Validate the format of the output
        status = self.validate_format(extracted)
        return status

    def validate_format(self, extracted: dict) -> bool:
        """
        Validates and cleans a dictionary of extracted fields.
        
        Args:
            extracted (dict): A dictionary of raw key-value pairs to validate.
                              Example:
                              {
                                  'order_number': 'ORD78901',
                                  'category': 'shipping',
                                  'description': 'Some description',
                                  'urgency': 'high'
                              }
        
        Returns:
            bool: True if all fields are valid, False if any fields were invalid (and removed).

        Side Effects:
            - Updates self.extracted with valid, cleaned fields.
            - Removes invalid keys from the `extracted` argument.
            - Optionally prints detailed logs if `verbose=True`.
        """
        invalid_keys = []
        for key, value in extracted.items():
            is_valid, cleaned = validate_and_extract(key, value, self.lang)   
            if not is_valid:
                invalid_keys.append(key)
                if self.verbose:
                    print(f"[VALIDATION] ❌ {key}='{value}' is invalid.")
            else:
                extracted[key] = cleaned
                if self.verbose:
                    print(f"[VALIDATION] ✅ {key}='{value}' is valid.")
        
        # Remove invalid keys from the dictionary
        for key in invalid_keys:
            extracted.pop(key, None)

        # Check for missing required keys
        missing_keys = [key for key in self.required_keys if key not in extracted]
        if missing_keys:
            if self.verbose:
                print(f"⚠️ Missing required keys: {missing_keys}")
            return False

        if not invalid_keys:
            if self.verbose:
                print("✅ All fields passed local validation.")
            return True
        else:
            if self.verbose:
                print(f"⚠️ Some fields were removed during validation: {invalid_keys}")
        
        return not invalid_keys