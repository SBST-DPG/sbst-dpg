<h2>SBST-DPG</h2><br>
Defect prediction guided search-based software testing (SBST-DPG) combines defect prediction and search-based software testing (SBST) to focus the test generation towards the defective classes in a project. SBST-DPG consists of three modules: i) Defect Predictor, ii) Budget Allocation Based on Defect Scores (BADS) and iii) SBST.
![image](https://user-images.githubusercontent.com/23715184/138988697-2f1f5665-8c31-4ae3-8c59-07271fbb97db.png)
By default, SBST-DPG uses Schwa as the defect predictor, which outputs the likelihoods of classes being defective (also called defect scores). 
Any defect predictor that outputs defect scores for the classes in the project would also be suitable for SBST-DPG.
BADS takes defect scores from the defect predictor and allocates time budgets to classes based on their likelihood of being defective.
We use EvoSuite with DynaMOSA as SBST and it runs test generation for all the classes with the allocated time budgets by BADS.
