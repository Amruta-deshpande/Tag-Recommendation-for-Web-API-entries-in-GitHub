import scalanlp.io._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.text.tokenize._;
import scalanlp.pipes.Pipes.global._;

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;


//Load the llda train model 
val modelPath = file("llda-cvb02-ecbea4c0-151-2b092511-8cb6e8e9");

println("Loading "+modelPath);
val model = LoadCVB0LabeledLDA(modelPath).asCVB0LDA;

/**
Tokenizer first tokenize on space and punctuation and lowercase everything.
Ignore all characters other than alphabets. Consider only those words with more 
than 3 charcetrs. 
**/ 

val source= CSVFile("total_test_data.csv")

/**
Read the source file only second column as it contain text
Tokenize with tokenizer on text. Ignore terms present in less than 4 
documents. Take terms with more than 5 documents.
**/

val text = {
  source ~>                             
  Columns(2) ~>
  Join(" ") ~>                          
  TokenizeWith(model.tokenizer.get)      
}

/**
Read the source file only first column as it contains labels
Tokenize with tokenizer on text. Ignore terms present in less than 4 
documents. Take terms with more than 10 documents.
**/ 

val labels = {
source ~>                              
Column(1) ~>                           
TokenizeWith(model.tokenizer.get) 
TermCounter()                       

}
val output = file(modelPath, source.meta[java.io.File].getName.replaceAll(".csv",""));
val dataset = LDADataset(text, model.termIndex);


println("Writing document distributions to "+output+"-document-topic-distributions-res.csv");
val perDocTopicDistributions = InferCVB0DocumentTopicDistributions(model, dataset);
CSVFile(output+"-document-topic-distributions-res.csv").write(perDocTopicDistributions);

println("Estimating per-doc per-word topic distributions");
val perDocWordTopicDistributions = EstimatePerWordTopicDistributions(model, dataset, perDocTopicDistributions);


//Extract top-terms from topic term distributions
println("Writing top terms to "+output+"-top-terms.csv");
val topTerms = QueryTopTerms(model, dataset, perDocWordTopicDistributions, numTopTerms=10);
CSVFile(output+"-top-terms.csv").write(topTerms);