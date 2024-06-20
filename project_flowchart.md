## Project Overview

```mermaid
graph TD;
    Start[SAT-AI] --> Dataset;
    Start[SAT-AI] --> Models;
    Dataset[Dataset for Remote Sensing] --> EarthVQA;
    Dataset --> RSVQA;
    Dataset --> otherdataset[Other Dataset];
    Models --> Model1[Zero Shot Segmentation Model];
    Models --> CogVLM; 
    Models --> othermodel[Other Model];
    othermodel[Other Model] --> FinetuneModel
    otherdataset --> FinetuneModel
    RSVQA --> FinetuneModel;
    EarthVQA --> FinetuneModel;
    CogVLM --> FinetuneModel;
    Model1 --> FinetuneModel;
    FinetuneModel --> |Accurate| finalmodel[Remote Sensing Model];
    FinetuneModel --> |Needs Work| othermodel;
    FinetuneModel --> |Needs Work| otherdataset;
    finalmodel --> |improve| FinetuneModel
    finalmodel --> |create interface| End