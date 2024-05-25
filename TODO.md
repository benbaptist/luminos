# Version Goals

## 0.15
- [ ] Google (and Google Gemini) model support
    - [ ] `google` will be the provider, three models will inherit it: `gemini-1.0-pro`, `gemini-1.5-flash`, `gemini-1.5-pro`
    - [ ] See other models' implementations to see how it should be implemented. Specifically, see how Ollama is implemented since it uses LiteLLM, and we should use LiteLLM to implement Google. See example in 'examples/gemini.py' for an example
- [ ] All errors should go through logger.error
- [ ] BUG FIX: Not accepting multi-line inputs at prompt, EOFs too soon and submits to AI
- [ ] BUG FIX: EOFError for input.py prompt needs to be try/caught separately from everything else - if EOFError is raised anywhere deeper in the AI logic pipeline, it thinks the user simply hit Ctrl+D and 'exits' the whole program. i.e. the scope of the try/except needs to be narrower.

# Unsorted Goals
- [ ] Save sessions in ~/.config/luminos, associate them with current directory, and prompt for recalling previous sessions upon launch. Show a list of old sessions and the option to either recall one or to proceed a fresh session
- [ ] Custom prompt templates/configs - have some sort of '.luminos_rc' file that can be read in the current directory, and upon launcing luminos, have it prompt if you'd like to utilize the luminos_rc prompt, which would help guide the LLM for the particular project, such as instructions for familiarizing yourself.
- [ ] Better permission prompt
    - [ ] Ability to deny permission with REASON, so you can explain to the LLM why you didn't give it the ability to do that action
    - [ ] More granular permission control
- [ ] Save sessions to ~/.config/luminos/sessions, remember them by directory, and prompt on launch if you want to load an existing session or start a new one
- [ ] Better code structure, more organized
- [ ] Handle token overflows properly
- [ ] Vision processing for supported models
- [ ] Two --verbose levels, for better control of debugging
- [ ] Better CLI elements
    - [ ] Spinning animation while LLM is generating
    - [ ] Ctrl+C during generation should interrupt the generation properly, returning you to a prompt
    - [ ] Up/down arrows should give you prompt history