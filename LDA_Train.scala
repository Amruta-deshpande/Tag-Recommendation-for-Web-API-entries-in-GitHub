import scalanlp.io._;
import scalanlp.text.tokenize._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.pipes.Pipes.global._;


//for LDA

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;
 

val source = CSVFile("train_data.csv") 

/**
Tokenizer first tokenize on space and punctuation and lowercase everything.
Ignore all characters other than alphabets. Consider only those words with more 
than 3 charcetrs. 
**/ 

val tokenizer = {
SimpleEnglishTokenizer() ~>    
CaseFolder() ~>                        
WordsAndNumbersOnlyFilter() ~>  
StopWordFilter("en") ~>  
MinimumLengthFilter(3)                 
}

/**
Read the source file only first and second column as it contain text
Tokenize with tokenizer on text. Ignore terms present in less than 4 
documents. Take terms with more than 5 documents.
**/

val text = {
source ~>                              
Columns(1,2) ~>
Join(" ") ~>                           
TokenizeWith(tokenizer) ~>             
TermCounter()  ~>                   
TermStopListFilter(List("access", "request", "requests", "methods","available","use","example","post","use","example","using","posts","services"))  
  

// Set K=40 based on the perplexity and define model parameters
val dataset = LDADataset(text);
val params = LDAModelParams(numTopics = 40, dataset = dataset);

//Train the Model to fit the document
//Name of the output model folder to generate
val modelPath = file("ldatrain-"+dataset.signature+"-"+params.signature);
TrainCVB0LDA(params, dataset, output=modelPath, maxIterations=200);
