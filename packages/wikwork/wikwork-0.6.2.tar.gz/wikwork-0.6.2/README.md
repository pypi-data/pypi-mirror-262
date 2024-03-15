# Summary
This package uses Wikimedia REST APIs to retrieve word and audio file
information from Wiktionary. There is also functionality to parse
the dictionary entries for German, Polish, and Czech words to extract
much of the page information as object attributes.

# Trademark Notice
Wiktionary, Wikimedia, Wikidata, Wikimedia Commons, and MediaWiki are
trademarks of the Wikimedia Foundation and are used with the permission of
the Wikimedia Foundation. We are not endorsed by or affiliated with the
Wikimedia Foundation.

# Wikimedia API Terms and Conditions
The REST APIs used are an interface provided by Wikimedia. The version
used is version 1. Global rules, content licensing, and terms of service set
by Wikimedia for using the APIs are currently at:
   https://[xx].wiktionary.org/api/rest_v1, where
[xx] is replaced by the language code of the Wiktionary (eg,
   https://en.wiktionary.org/api/rest_v1 for the English Wiktionary).

# Release Notes (v0.6.0)
- Add support for parsing Czech Wiktionary pages for grammar information. 
- For German words, put lines after the `{{Sinnverwandte Wörter}}` template
  into a new `related_words` attribute instead of in the synonyms attribute
  with the lines after the `{{Synonyme}}` template.
- Attributes that are not by definition derived from a single input line
  or template are now stored as a list of strings instead of a string joined
  on '; '. (The default csv files output by the wrapper still perform this
  join when writing the csv.)
- Attributes will not be overwritten for an entry. If a word page has 
  multiple section headings representing the same object attribute, only the
  first will be stored, with messages to the log generated for the rest.

# Release Notes (v0.6.1)
- Documentation corrections.

# Release Notes (v0.6.2)
- Bug fix. The last attribute for a word/entry was not being written if the
  wikitext file had a section for another language after the target language.

# Functionality
This package extracts word and audio file information (but not audio files
themselves) from Wiktionary. Support to download audio may be added in the
future. For German, Polish, and Czech words, the most common elements of the
dictionary entry or entries for a word can be extracted into separate
fields. Similar functionality may be added in the future for other
languages, or users can write their own parsers on the downloaded objects.

Downloading all audio files for a given headword (ie, page or page title)
technically only requires two REST API calls, one to get the list of audio
files for the headword and then to download the audio file. However, doing
this and nothing else would ignore the downloader's potential attribution
and other responsibilities imposed by the file licenses. Furthermore, the
audio files obtained from the media list API for a given headword should
consist of all audio files from the headword page, including those in
languages other than the one in which the Wiktionary is written.

The package therefore contains the following functionality:

1. Automatic removal of audio files that are likely (based on file naming
convention) not pronunciations in the target language.

2. Creation of a yes/no flag to indicate whether the audio file is
probably a pronunciation of the headword and not, say, an example
expression (again based on file naming conventions).

3. Assignment of probable authors, probable licenses, and probable
attributions (when audio file author/uploader specifies an attribution
parameter that differs from the author) based on parsing the wikitext of
the file that is
meant to contain such information. The parsing of such text files may not
be perfect, and therefore users should review these assigned elements
with the wikitext to confirm the necessary information was correctly extracted.
A wrapper function is provided to print the probable license, probable author,
probable attribution, and wikitext to a single file for easier review.
Users should also check that the templates that hold license and author
information for their selected audio files still have the same parameters
and interpretation as when the default parser was written.

4. Support for user-created functions that assign the probable authors,
probable licenses, and probable attributions for users that want to write their
own parser or write a wrapper around a parser from a different third-party
package.

5. Sorting of audio files by user-defined keys (which might include sorting
by preferred probable licenses, probable authors, language variants [eg,
American vs British English], or pronunciations).

6. Creation of cache/output directories that will store downloaded HTML and
wikitext information. Users can configure whether or not to use the cache.
Page revision is part of the key when retrieving from the cache, so
deletion of the cache files with the revision information will result in
the latest revision number being retrieved. If the revision is not changed
and reading from the cache is configured, the program will know there is
no need to re-update the media list or HTML/wikitext output for the page.

7. An easy-to-use wrapper that downloads headword and audio file
information into objects, and then optionally outputs the results in a
text file at the word or audio file level.

8. Support to sleep a specified amount of time after a REST API call to
comply with Wikimedia™ rate limits.

9. Logging using the `logging` package is used in the standard manner
with a null handler attached in the `__init__.py`.

10. Support for `GermanWord` objects, which are like `Headword` objects, but
have an additional list of grammar information for each dictionary entry (ie,
for each third-level heading in the page). The information extracted includes:
word separation information, pronunciations, abbreviations, definitions,
origins, synonyms, opposites, hyponyms, hypernyms, examples, expressions,
characteristic word combinations, word formations, references and additional
information, sources, alternate spellings, sayings/proverbs, comparative and
superlative form(s) of adjectives, verb forms (first, second and third person
singular present, first/third singular preterite, past participle, helper
verb, and the Subjunctive II [Konjuntiv II]), the usual 8 noun declinations
(4 cases by singular/plural) and whether the noun declines as an adjective).
Note that the page information is broken up into the sections above, but
the wikitext is not completely transcluded (ie, replaced with plain text).

11. Support for `PolishWord` objects, which are like `Headword` objects,
but have an additional list of over sixty attributes with grammar information
for the dictionary entry. The information extracted includes: pronunciations,
definitions, etymology, synonyms, antonyms, hyponyms, hypernyms, examples,
expressions, word combinations, word formations, references, syntax,
meronyms, holonyms, and cautions. Up to two comparative forms for the
adjective are presented, along with over 15 verb conjugated or
derived forms, noun gender (both as {'m','f','n'} and also as subcategories
for the masculine nouns by person, animal, and/or thing.), and the usual
14 declinations (7 cases by singular/plural).  Note that the page information
is broken up into the sections listed above, but the wikitext is not
completely transcluded (ie, replaced with plain text).

12. Support for `CzechWord` objects, which are like `Headword` objects,
but have an additional list of over sixty attributes with grammar information
for the dictionary entry. The information extracted includes at the word
level: pronunciations, word separations, etymology, external links, variants,
and references. At the entry level, attributes include: definitions, 
etymology (if differs by entry), synonyms, antonyms, examples, expressions,
sayings, related words, variants, word combinations, abbreviations, 
declensions, collocations, and part of speech summary and detail information.
Up to two comparative forms for the adjective are presented, along with almost
30 verb conjugated or derived forms, noun gender (both as {'m','f','n'} and
also as subcategories for the masculine nouns by animate/inanimate, and the 
usual 14 noun declinations (7 cases by singular/plural).  Note that the page
information is broken up into the sections listed above, but the wikitext is
not completely transcluded (ie, replaced with plain text).

In the future (potentially), users can record their decision about
whether to request download of an audio file and pass the decision back
into package objects or functions to select files for download. Currently,
the decision will be stored in the object but will not cause downloading
until the package is updated to support this.

# Example
```
from wikwork import wrapper, page_media, io_options
import logging

# set up the logger to print to the console
logger = logging.getLogger('wikwork')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

my_headers = {
    'User-Agent': '(wikwork Python package) (email or phone)'
}

io_opts = io_options.IOOptions(
     output_dir='cache_output/de',
     project='Wiktionary',
     headers=my_headers)

# Sort first by pronunciation not from Austria, then by whether the audio
# is likely a pronuncation of only the headword, then by preferred license
# status, then by pronunciation (as German words ending in '-ig' often
# have two variants recorded, so this preferentially selects those
# sounding like '-ik' [IPA: -ɪk] over '-isch' [IPA: -ɪç]).

pref_license_set = set(['cc-by-sa 4.0', 'cc-by-sa-4.0'])

def my_sort(x: page_media.AudioFile):
     return (not x.filename.startswith('De-at-'),
     x.prob_headword,
     (x.prob_licenses is not None and
       len(set(x.prob_licenses) & pref_license_set)>0),
     re.search('ɪk/', x.wikitext) is not None)

# can use the wrapper, (de_input.txt has a column with header = 'Word'
# and then rows with values given by input_list).

input_list = ['Kind','Montag','helfen','Zahl','Wunderbar!',
              'rot','sonnig','zum Beispiel']

res = wrapper.words_wrapper(
     input_words_filename=f'de_input.txt',
     headword_lang_code='de',
     audio_html_lang_code='en',
     io_options=io_opts,
     input_words_column_name='Word',
     fetch_word_page=True,
     fetch_audio_info=True,
     sort_key=my_sort,
     output_words_filename='de_output_words.txt',
     output_audios_filename='de_output_audios.txt',
     output_wikitext_filename='de_wiki.txt'
     )

# ... do other things with res if desired ...

# ... or instead of using the wrapper, create Headword objects directly ...
# (One could also make german.GermanWord objects instead of Headword objects.
# The difference is GermanWord objects will parse the wikitext of the headword
# page for grammar information. See german.GermanWord for details.)

res2 = []
for word in input_list:
    word_info = page_media.Headword(headword=word, lang_code='de')
    if word_info.valid_input:
        # need to get revision info first
        word_info.fetch_revision_info(io_options=io_opts)
        # optionally get word_page (https://de.wiktionary.org/wiki/foo)
        word_info.fetch_word_page(io_options=io_opts)
        # optionally get list of audio files and their info from from
        #    (https://en.wiktionary.org/wiki/File:audio_filename.ogg)
        word_info.fetch_audio_info(io_options=io_opts,
            audio_html_lang_code='en', sort_key=my_sort)
        # ... whatever else user wants to do ...
        res2.append(word_info)
```
# Other Considerations
1. The following page has other useful points to consider when deciding
whether or how to use downloaded media:
    https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia

2. Users should familiarize themselves with wikitext and especially
templates.  For example, the file-namespace pages with license/author
information are typically quite small (<100 characters). The 'Template:'
namespace on Wikimedia Commons™ can be used to find information about a
template (ie, strings enclosed in two braces '{{...}}'. For example, information
about the template '{{cc-zero}}' can be found at
    https://commons.wikimedia.org/wiki/Template:cc-zero (which redirects to
    https://commons.wikimedia.org/wiki/Template:Cc-zero).
One would expect these templates to not change much over time (the one
linked above was changed only four times from when it was protected in
October 2013 to February 2024).

3. There may be other methods of retrieving license information, perhaps
through MediaWiki™ action APIs or Wikidata™. For action APIs, it does seem
to be possible with images.

4. Determining which template parameters to assign to which attributes was
based on researching templates at the time of writing the function that
parses such templates. Templates are not retrieved 'in real time' by the
package at the time of function execution. Information in the docstrings of
the relevant `GermanEntry` or `PolishEntry` objects indicate the source
parameter for all such attributes so that users can verify at the time of
program execution, if desired, the meaning of the parameter has not changed.

5. Users planning a very large number of requests might be better off using
a database dump.

# Known issues
The media list REST API call for the Spanish Wiktionary returns information
about very few audio files compared to what is available on the headword
page.  Presumably whatever parser the REST API call uses to extract the
media list doesn't recognize the template the files are nested in.
