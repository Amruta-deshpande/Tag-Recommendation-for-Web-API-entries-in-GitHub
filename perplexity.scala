// Stanford TMT Example 5 - Selecting LDA model parameters
// http://nlp.stanford.edu/software/tmt/0.4/

// tells Scala where to find the TMT classes
import scalanlp.io._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.text.tokenize._;
import scalanlp.pipes.Pipes.global._;

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;

val source = CSVFile("total_perplexity_data.csv")]

/**
Tokenizer first tokenize on space and punctuation and lowercase everything.
Ignore all characters other than alphabets. Consider only those words with more 
than 3 charcetrs. 
**/ 

val tokenizer = {
  SimpleEnglishTokenizer() ~>            
  CaseFolder() ~>                        
  WordsAndNumbersOnlyFilter() ~>         
  MinimumLengthFilter(3)                 
}

/**
Read the source file only second column as it contain text
Tokenize with tokenizer on text. Ignore terms present in less than 4 
documents. Take terms with more than 5 documents.
**/
val text = {
  source ~>                              
  Column(2) ~>                           
  TokenizeWith(tokenizer) ~>             
  TermCounter() ~>                       
  TermMinimumDocumentCountFilter(4) ~>   
  DocumentMinimumLengthFilter(5)         
}
//Divide data into training and testing data
val train_data = text.data.size * 4 / 5;

// build a training dataset
val training = LDADataset(text ~> Take(train_data));
 
// build a test dataset, using term index from the training dataset 
val testing  = LDADataset(text ~> Drop(numTrain));

// a list of pairs of (number of topics, perplexity)
var scores = List.empty[(Int,Double)];

// Check for various number of topics


  for (numTopics <- List(15,20,25,30,35,40,45)) {
  val params = LDAModelParams(numTopics = numTopics, dataset = training);


  val modelPath = file("lda-"+training.signature+"-"+params.signature);
  val model = TrainCVB0LDA(params, training, output=modelPath, maxIterations=100);
  
  println("[perplexity] computing at "+numTopics);

  val perplexity = model.computePerplexity(testing);
  
  println("[perplexity] perplexity at "+numTopics+" topics: "+perplexity);

  scores :+= (numTopics, perplexity);
}

for ((numTopics,perplexity) <- scores) {
  println("[perplexity] perplexity at "+numTopics+" topics: "+perplexity);
}

