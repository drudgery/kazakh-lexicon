# kazakh-lexicon
Code to create lexicon json from sentence json

## Steps to generate lexicon 

- Python virtual environment
    
        python3 -m venv venv
- Activate venv
        
        source venv/bin/activate
- Install dependencies
        
        pip install -r requirements.txt
- Run kazakh_lexicon.py file and provide the required paths for input and output files
        
        python3 kazakh_lexicon.py


## NOTE

1. If the input file contains multiple entries of exactly same token in a given sentence, the program processes the first entry and skips the rest. If the same token is repeated more than once at different positions in the same sentence then they are considered separate occurrences and processed independently.

2. Lemmas with same canonical form but different pos are considered separate lemmas and have separate entries.

Both of these behaviours could be adjusted, if required.