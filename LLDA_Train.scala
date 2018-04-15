import scalanlp.io._;
import scalanlp.text.tokenize._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.pipes.Pipes.global._;


//for Labeled LDA

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;


val source=CSVFile("total_train_data.csv")
println("Success: " + source + " contains " + source.data.size + " records"); 

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



/**
Read the source file only second column as it contain text
Tokenize with tokenizer on text. Ignore terms present in less than 4 
documents. Take terms with more than 5 documents.
**/

val text = {
source ~>                              
Columns(2) ~>                          
Join(" ") ~>                           
TokenizeWith(tokenizer) ~>            
TermCounter()   ~>
DocumentMinimumLengthFilter(2)         
}

/**
Read the source file only first column as it contains labels
Tokenize with tokenizer on text. Ignore terms present in less than 4 
documents. Take terms with more than 10 documents.
**/


val labels = {
source ~>                              
Column(1) ~>                          
TokenizeWith(tokenizer) ~>            
TermCounter()                          
// TermMinimumDocumentCountFilter(5)    
}

val dataset = LabeledLDADataset(text, labels);


// define the model parameters
val modelParams = LabeledLDAModelParams(dataset=dataset);

// Name of the output model folder to generate
val modelPath = file("llda-cvb02-"+dataset.signature+"-"+modelParams.signature);

// Trains the model, write to the output of file

TrainCVB0LabeledLDA(modelParams, dataset, output = modelPath, maxIterations = 200);

// 