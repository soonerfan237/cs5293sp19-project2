Here is an example command to run the unredactor:
pipenv run python project2/unredactor.py 'aclImdb/test_redacted/neg/7*.txt'

The command line argument should be the files that you wish to unredact.  You can pass files that are already redacted.  This is detected by looking for a .redacted extension.  If you pass files that have not been redacted yet, the code will automatically redact names from the files and store the results in the same location with a .redacted extension.

When redacting names, the code will use nltk to look for chunks that have the PERSON tag.  Those chunks will be replaced by a series of Xs in the redacted files.  Spaces will be preserved.

The set of training files is hardcoded to the aclImdb folder.  The code will train on a set of files that is half neg and half pos.  It will parse each file for PERSON names and then generate a set of features for each name.  If there are multiple names in a review, it will generate features for each name separately.

My code generates the following features.  The first feature is the length of the review.  I take the number of characters in the review and divide by 10 to reduce the order of magnitude.  This is useful so the range of value is smaller while training - this helps overfitting the data.  The second feature is the length of the name.  The third is the number of spaces in the name.  And finally, there is a feature for the sentiment of the review.  This is obtained from the pos/neg folder names.  If no sentiment is available, that is another category.

After generating the featureset for each name, it is run through a NaiveBayes classifier using nltk.  

The code will then process each file specified in the command ine argument - using the redacted version.  It will generate the set of features for each entity and then nltk will attempt to classify the correct name.

For validation, the code will look for the corresponding unredacted file and find the actual name.  The code generates statistics for the total number of predictions and the number that were correct.
