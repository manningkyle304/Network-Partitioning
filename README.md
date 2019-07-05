# Network-Partitioning


The code in "network_partitioning.py" is a portion of the code that was used for an assignment in an algorithms class. The code uses ideas from the description document, "hw2_description_document.pdf", as well as from section 3.6b in the book Networks, Crowds, and Markets (contained in "chapter_3.pdf"). 

To summarize, the goal of the project is to partition graphs such that the underlying community structure is preserved, so as to identify subgroups within communities. In order to do so, we remove edges of high "betweenness", until a stopping criterion is reached. To calculate betweenness, we must compute the flow over all edges in a graph - this is implemented in the function "compute_flow". 
