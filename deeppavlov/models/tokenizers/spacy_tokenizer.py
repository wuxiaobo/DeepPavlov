"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import spacy
import re

from deeppavlov.core.models.component import Component
from deeppavlov.core.common.registry import register


@register('spacy_tokenizer')
class SpacyTokenizer(Component):

    def __init__(self, *args, **kwargs):
        self.NLP = spacy.load('en')

    def _tokenize(self, text, **kwargs):
        """Tokenize with spacy, placing service words as individual tokens."""
        return [t.text for t in self.NLP.tokenizer(text)]

    def _detokenize(self, tokens):
        """
        Detokenizing a text undoes the tokenizing operation, restoring
        punctuation and spaces to the places that people expect them to be.
        Ideally, `detokenize(tokenize(text))` should be identical to `text`,
        except for line breaks.
        """
        text = ' '.join(tokens)
        step0 = text.replace('. . .',  '...')
        step1 = step0.replace("`` ", '"').replace(" ''", '"')
        step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
        step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
        step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
        step5 = step4.replace(" '", "'").replace(" n't", "n't")\
            .replace(" nt", "nt").replace("can not", "cannot")
        step6 = step5.replace(" ` ", " '")
        return step6.strip()

    def __call__(self, batch):
        if isinstance(batch[0], str):
            return [self._tokenize(sent) for sent in batch]
        if isinstance(batch[0], list):
            return [self._detokenize(sent) for sent in batch]
        raise TypeError("SpacyTokenizer.__call__() not implemented for `{}`".format(type(batch[0])))
