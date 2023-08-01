import json
from typing import List, Optional
from pydantic import BaseModel, ValidationError


class LemmaForm(BaseModel):
    '''Class for representation of the forms of Lemma'''
    formId: int
    form: str
    feats: Optional[str]
    freq: int


class Lemma(BaseModel):
    '''Class for lemma data structure'''
    lemmaId: int
    lemma: str
    freq: int
    pos: str
    pos_finegrained: str
    forms: List[LemmaForm]


class LemmaCollection(BaseModel):
    lemmas: List[Lemma]


class Token(BaseModel):
    '''Class for token data structure'''
    id: str
    text: str
    lemma: str
    pos: str
    pos_finegrained: str
    feats: Optional[str]
    start_char: str
    end_char: str


class Sentence(BaseModel):
    '''Class for sentence data structure'''
    sentence_text: str
    tokens: List[Token]


def get_lemmas(sentences, lemma_id=1):
    '''
        An entry per lemma for all lemmas in the sentences
        The part of speech label and all inflection information per lemma
        A total frequency count for each lemma
        A total frequency count for each wordform per lemma
    '''
    processed_lemmas = {}
    for sentence in sentences:
        processed_tokens = []
        tokens = sentence.tokens

        for token in tokens:
            print("Token type", type(token), token.text)
            if token not in processed_tokens:
                form_freq_updated = False
                processed_tokens.append(token)

                lemma_text = token.lemma
                lemma_pos = token.pos
                lemma_pos_finegrained = token.pos_finegrained
                lemma_feats = token.feats
                current_lemma_form = token.text

                basic_lemma = tuple((lemma_text, lemma_pos))

                if basic_lemma in processed_lemmas:
                    lemma_entry = processed_lemmas[basic_lemma]
                    lemma_entry.freq += 1

                    lemma_forms = lemma_entry.forms
                    for lemma_form in lemma_forms:
                        if lemma_form.form == current_lemma_form and lemma_form.feats == lemma_feats:
                            lemma_form.freq += 1
                            form_freq_updated = True
                    if not form_freq_updated:
                        lemma_form = LemmaForm(
                            form=current_lemma_form,
                            feats=token.feats,
                            freq=1,
                            formId=len(lemma_forms)+1
                        )
                        lemma_forms.append(lemma_form)
                else:
                    lemma_form = LemmaForm(
                        form=current_lemma_form,
                        feats=lemma_feats,
                        freq=1,
                        formId=1
                    )
                    lemma_entry = Lemma(
                        lemmaId=lemma_id,
                        lemma=lemma_text,
                        freq=1,
                        pos=lemma_pos,
                        pos_finegrained=lemma_pos_finegrained,
                        forms=[lemma_form]
                    )

                    processed_lemmas[basic_lemma] = lemma_entry
                    lemma_id += 1

    all_lemmas = LemmaCollection(lemmas=processed_lemmas.values())

    return all_lemmas


def get_lemmas_from_json_file(input_file, output_file):
    with open(input_file, 'r') as read_json_file:
        data = json.load(read_json_file)
        try:
            print("Getting sentences")
            sentences = [Sentence(**item) for item in data['sentences']]
            print("Getting Lemmas")
            all_lemmas = get_lemmas(sentences).model_dump()
            # Write data to a JSON file
            with open(output_file, 'w') as write_json_file:
                json.dump(all_lemmas, write_json_file,
                          ensure_ascii=False, indent=2)
        except ValidationError as exc:
            print(exc.json())


def main():
    """Main function."""

    # sample_parsed_sentences.json
    input_file = input("Enter input file path: ")

    # kazakh_lexicon.json
    output_file = input("Enter output file path: ")

    get_lemmas_from_json_file(input_file, output_file)


if __name__ == "__main__":
    main()
