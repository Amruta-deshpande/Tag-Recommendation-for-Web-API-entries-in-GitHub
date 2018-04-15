//Loading the trained model
import scalanlp.io._;
import scalanlp.text.tokenize._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.pipes.Pipes.global._;

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;


//Take the train model path and load it using CVB0
val modelPath = file("ldatrain-b574ad2e-40-2de4510c");
println("Loading "+modelPath);
val model = LoadCVB0LDA(modelPath);


// val source = CSVFile("api_data.csv") 
val source = CSVFile("test_data.csv") 


/**
Tokenizer first tokenize on space and punctuation and lowercase everything.
Ignore all characters other than alphabets. Consider only those words with more 
than 3 charcetrs. 
**/ 

val text = {
source ~>                   
Columns(2) ~>  
Join(" ") ~>                  
TokenizeWith(model.tokenizer.get)        
// Base name of output files to generate

val output = file(modelPath, source.meta[java.io.File].getName.replaceAll(".csv",""));

// turn the text into a dataset ready to be used with LDA
val dataset = LDADataset(text, termIndex = model.termIndex);

println("Writing document distributions to "+output+"-document-topic-distributions.csv");
val perDocTopicDistributions = InferCVB0DocumentTopicDistributions(model, dataset);
CSVFile(output+"LDA-document-topic-distributuions.csv").write(perDocTopicDistributions);


//usage
println("Writing topic usage to "+output+"LDA-usage.csv");
val usage = QueryTopicUsage(model, dataset, perDocTopicDistributions);
CSVFile(output+"LDA-usage.csv").write(usage);

//per wword topic distribution
println("Estimating per-doc per-word topic distributions");
val perDocWordTopicDistributions = EstimatePerWordTopicDistributions(model, dataset, perDocTopicDistributions);
//top-terms
println("Writing top terms to "+output+"-top-terms.csv");
val topTerms = QueryTopTerms(model, dataset, perDocWordTopicDistributions, numTopTerms=10);
CSVFile(output+"LDA-top-terms.csv").write(topTerms);

