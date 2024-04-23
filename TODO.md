# Short-Term Goals 
- [ ] Better configuration file, more organized
- [ ] Default config file should be minimalistic, config.py should stop populating unpopulated fields
- [ ] Ctrl+C during generation should interrupt the generation properly
- [ ] Up/down arrows should give you prompt history
- [ ] All errors should go through logger.error
- [ ] logger.level should be color-formattated according to the logging level
- [ ] Spinning animation while LLM is generating

# Long-Term Goals
- [ ] Save sessions in ~/.config/luminos, associate them with current directory, and prompt for recalling previous sessions upon launch. Show a list of old sessions and the option to either recall one or to proceed a fresh session
- [ ] Custom prompt templates/configs - have some sort of '.luminos_rc' file that can be read in the current directory, and upon launcing luminos, have it prompt if you'd like to utilize the luminos_rc prompt, which would help guide the LLM for the particular project, such as instructions for familiarizing yourself.
- [ ] Better permission prompt
    - [ ] Detailed preview of permission request if specified, use nano/vi to showcase it. 
    - [ ] Ability to deny permission with REASON, so you can explain to the LLM why you didn't give it the ability to do that action
    - [ ] More granular permission control
- [ ] Save sessions to ~/.config/luminos/sessions, remember them by directory, and prompt on launch if you want to load an existing session or start a new one
- [ ] Better code structure, more organized
- [ ] Handle token overflows properly
- [ ] Vision processing for supported models
- [ ] Two --verbose levels, for better control of debugging
- [X] Fully implement Anthropic API