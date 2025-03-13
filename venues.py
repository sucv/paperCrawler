## These venues have an average citation number per paper greater than 10.
# Based on https://www.cs.cornell.edu/andru/csconf.html

venue_dblp_url_dict = {
    # ---------------------------------------------------
    # Theory of computation
    # ---------------------------------------------------
    "ACM Symposium on Theory of Computing (STOC)": "https://dblp.org/db/conf/stoc",
    "IEEE Symposium on Foundations of Computer Science (FOCS)": "https://dblp.org/db/conf/focs",
    "Journal of the ACM (JACM)": "https://dblp.org/db/journals/jacm",
    "SIAM Journal on Computing (SIAMCOMP)": "https://dblp.org/db/journals/siamcomp",
    "Logic in Computer Science (LICS)": "https://dblp.org/db/conf/lics",
    "Computational Learning Theory (COLT)": "https://dblp.org/db/conf/colt",
    "International Colloquium on Automata, Languages and Programming (ICALP)": "https://dblp.org/db/conf/icalp",
    "Theory and Applications of Satisfiability Testing": "https://dblp.org/db/conf/sat",

    # ---------------------------------------------------
    # Information and coding theory
    # ---------------------------------------------------
    "IEEE Transactions on Information Theory (TIT)": "https://dblp.org/db/journals/tit",

    # ---------------------------------------------------
    # Data structures and algorithms
    # ---------------------------------------------------
    "ACM-SIAM Symposium on Discrete Algorithms (SODA)": "https://dblp.org/db/conf/soda",
    "ACM Symposium on Parallel Algorithms and Architectures (SPAA)": "https://dblp.org/db/conf/spaa",
    "Symposium on Computational Geometry (SOCG)": "https://dblp.org/db/conf/compgeom",

    # ---------------------------------------------------
    # Programming language theory and formal methods
    # ---------------------------------------------------
    "ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL)": "https://dblp.org/db/conf/popl",
    "SIGPLAN Conference on Programming Language Design and Implementation (PLDI)": "https://dblp.org/db/conf/pldi",
    "ACM Transactions on Programming Languages and Systems (TOPLAS)": "https://dblp.org/db/journals/toplas",
    "Tools and Algorithms for Construction and Analysis of Systems (TACAS)": "https://dblp.org/db/conf/tacas",
    "European Symposium on Programming (ESOP)": "https://dblp.org/db/conf/esop",
    "International Workshop on Model Checking of Software (SPIN)": "https://dblp.org/db/conf/spin",
    "Computer Aided Verification (CAV)": "https://dblp.org/db/conf/cav",
    "Symposium on Code Generation and Optimization (CGO)": "https://dblp.org/db/conf/cgo",
    "Static Analysis Symposium/Workshop on Static Analysis (SAS(WSA))": "https://dblp.org/db/conf/sas",
    "VMCAI (Verification, Model Checking and Abstract Interpretation)": "https://dblp.org/db/conf/vmcai",
    "Hybrid Systems": "https://dblp.org/db/conf/hybrid",  # Often “HSCC”

    # ---------------------------------------------------
    # Computer graphics and visualization
    # ---------------------------------------------------
    "ACM Transactions on Graphics / SIGGRAPH (TOG)": "https://dblp.org/db/journals/tog",
    "Symposium on Computer Animation (SCA)": "https://dblp.org/db/conf/sca",
    "Eurographics Symposium on Rendering (EGSR)": "https://dblp.org/db/conf/egsr",
    "IEEE Visualization": "https://dblp.org/db/conf/visualization",
    "ACM Symposium on Interactive 3D Graphics (I3D)": "https://dblp.org/db/conf/i3d",
    "IEEE Symposium on Information Visualization (INFOVIS)": "https://dblp.org/db/conf/infovis",
    "Graphics Interface (GI)": "https://dblp.org/db/conf/graphicsinterface",
    "VisSym (Joint Eurographics - IEEE TCVG Symposium on Visualization)": "https://dblp.org/db/conf/vissym",

    # ---------------------------------------------------
    # Image and sound processing
    # ---------------------------------------------------
    "International Journal of Computer Vision (IJCV)": "https://dblp.org/db/journals/ijcv",
    "IEEE Transactions on Pattern Analysis and Machine Intelligence (PAMI)": "https://dblp.org/db/journals/pami",
    "IEEE Transactions on Speech and Audio Processing": "https://dblp.org/db/journals/tsap",
    "Computer Vision and Pattern Recognition (CVPR)": "https://dblp.org/db/conf/cvpr",
    "Audio- and Video-Based Biometric Person Authentication (AVBPA)": "https://dblp.org/db/conf/avbpa",
    "Computer Vision and Image Understanding (CVIU)": "https://dblp.org/db/journals/cviu",
    "IEEE Transactions on Image Processing": "https://dblp.org/db/journals/tip",
    "Pattern Recognition (PR)": "https://dblp.org/db/journals/pr",
    "Image and Vision Computing (IVC)": "https://dblp.org/db/journals/ivc",
    "IEEE Transactions on Multimedia (TMM)": "https://dblp.org/db/journals/tmm",
    "IEEE Transactions on Circuits and Systems for Video Technology (TCSV)": "https://dblp.org/db/journals/tcsvt",
    "International Symposium/Conference on Music Information Retrieval (ISMIR)": "https://dblp.org/db/conf/ismir",
    "Real-time Imaging": "https://dblp.org/db/journals/rti",

    # ---------------------------------------------------
    # Computational science, finance and engineering
    # ---------------------------------------------------
    "Mathematics of Computation": "https://dblp.org/db/journals/mcom",
    "Annual Reviews in Control": "https://dblp.org/db/journals/arc",
    "Automatica": "https://dblp.org/db/journals/automatica",
    "Transportation Science": "https://dblp.org/db/journals/transci",
    "Operations Research": "https://dblp.org/db/journals/or",
    "Foundations of Computational Mathematics (FoCM)": "https://dblp.org/db/conf/focm",
    "in Silico Biology (ISB)": "https://dblp.org/db/journals/isb",
    "Pacific Symposium on Biocomputing": "https://dblp.org/db/conf/psb",
    "Journal of Computational Biology (JCB)": "https://dblp.org/db/journals/jcb",
    "Bioinformatics / Computer Applications in the Biosciences (BIOINFORMATICS)": "https://dblp.org/db/journals/bioinformatics",
    "Intelligent Systems in Molecular Biology (ISMB)": "https://dblp.org/db/conf/ismb",
    "Briefings in Bioinformatics (BIB)": "https://dblp.org/db/journals/bib",
    "European Conference on Computational Biology (ECCB)": "https://dblp.org/db/conf/eccb",

    # ---------------------------------------------------
    # Human–computer interaction
    # ---------------------------------------------------
    "User Interface Software and Technology (UIST)": "https://dblp.org/db/conf/uist",
    "Human-Computer Interaction (journal/conference)": "https://dblp.org/db/journals/hci",
    "Computer Supported Cooperative Work (CSCW) – both journal & conference": "https://dblp.org/db/conf/cscw",
    "User Modeling and User-Adapted Interaction (UMUAI)": "https://dblp.org/db/journals/umuai",
    "International Journal of Human-Computer Studies (IJMMS)": "https://dblp.org/db/journals/ijmms",
    "IEEE Pervasive Computing": "https://dblp.org/db/journals/pervasive",

    # ---------------------------------------------------
    # Software engineering
    # ---------------------------------------------------
    "IEEE Transactions on Software Engineering (TSE)": "https://dblp.org/db/journals/tse",
    "ACM Transactions on Software Engineering and Methodology (TOSEM)": "https://dblp.org/db/journals/tosem",
    "European Software Engineering Conference (ESEC)": "https://dblp.org/db/conf/esec",
    "Requirements Engineering (RE)": "https://dblp.org/db/journals/re",
    "Software and System Modeling (SOSYM)": "https://dblp.org/db/journals/sosym",
    "Aspect-Oriented Software Development (AOSD)": "https://dblp.org/db/conf/aosd",
    "IEEE International Software Metrics Symposium (METRICS)": "https://dblp.org/db/conf/metrics",
    "Empirical Software Engineering (ESE)": "https://dblp.org/db/journals/ese",

    # ---------------------------------------------------
    # Artificial intelligence
    # ---------------------------------------------------
    "Journal of Artificial Societies and Social Simulation (JASSS)": "https://dblp.org/db/journals/jasss",
    "Journal of Machine Learning Research (JMLR)": "https://dblp.org/db/journals/jmlr",
    "Neural Information Processing Systems (NIPS)": "https://dblp.org/db/conf/nips",
    "International Conference on Machine Learning (ICML)": "https://dblp.org/db/conf/icml",
    "Artificial Intelligence (AI)": "https://dblp.org/db/journals/ai",
    "Journal of Artificial Intelligence Research (JAIR)": "https://dblp.org/db/journals/jair",
    "Uncertainty in Artificial Intelligence (UAI)": "https://dblp.org/db/conf/uai",
    "Meeting of the Association for Computational Linguistics (ACL)": "https://dblp.org/db/conf/acl",
    "North American Chapter of the Association for Computational Linguistics (NAACL)": "https://dblp.org/db/conf/naacl",
    "Computational Linguistics (COLI)": "https://dblp.org/db/journals/coli",
    "International Semantic Web Conference (ISWC)": "https://dblp.org/db/conf/semweb",
    "Principles of Knowledge Representation and Reasoning (KR)": "https://dblp.org/db/conf/kr",
    "Autonomous Agents and Multi-agent Systems (AAMAS)": "https://dblp.org/db/conf/atal",
    "JSAI Workshops (Japanese Society for AI)": "https://dblp.org/db/conf/jsai",
    "International Joint Conference on Artificial Intelligence (IJCAI)": "https://dblp.org/db/conf/ijcai",
    "Machine Learning (ML)": "https://dblp.org/db/journals/ml",
    "Neural Computation": "https://dblp.org/db/journals/neco",
    "IEEE Transactions on Neural Networks": "https://dblp.org/db/journals/tnn",
    "Journal of Field Robotics (JFR)": "https://dblp.org/db/journals/jfr",
    "International Journal of Robotic Research (IJRR)": "https://dblp.org/db/journals/ijrr",
    "IEEE Transactions on Robotics and Automation": "https://dblp.org/db/journals/trob/index.html",
    "IEEE Transactions on Robotics (TRob)": "https://dblp.org/db/journals/tro",
    "IEEE Transactions on Evolutionary Computation (TEC)": "https://dblp.org/db/journals/tevc",
    "IEEE Transactions on Fuzzy Systems (TFS)": "https://dblp.org/db/journals/tfs",
    "Knowledge Engineering Review (KER)": "https://dblp.org/db/journals/ker",

    # ---------------------------------------------------
    # Computer architecture and microarchitecture
    # ---------------------------------------------------
    "International Symposium on Microarchitecture (MICRO)": "https://dblp.org/db/conf/micro",
    "International Symposium on Computer Architecture (ISCA)": "https://dblp.org/db/conf/isca",
    "International Symposium on High-Performance Computer Architecture (HPCA)": "https://dblp.org/db/conf/hpca",
    "Architectural Support for Programming Languages and Operating Systems (ASPLOS)": "https://dblp.org/db/conf/asplos",
    "ACM SIGARCH Computer Architecture News": "https://dblp.org/db/journals/sigarch",
    "International Conference on Computer-Aided Design (ICCAD)": "https://dblp.org/db/conf/iccad",
    "International Symposium on Physical Design (ISPD)": "https://dblp.org/db/conf/ispd",

    # ---------------------------------------------------
    # Concurrent, parallel and distributed computing
    # ---------------------------------------------------
    "ACM Symposium on Operating Systems Principles (SOSP)": "https://dblp.org/db/conf/sosp",
    "Operating Systems Design and Implementation (OSDI)": "https://dblp.org/db/conf/osdi",
    "Networked Systems Design and Implementation (NSDI)": "https://dblp.org/db/conf/nsdi",
    "Workshop on Hot Topics in Operating Systems (HotOS)": "https://dblp.org/db/conf/hotos",
    "Principles and Practice of Parallel Programming (PPoPP)": "https://dblp.org/db/conf/ppopp",
    "International Conference on Distributed Computing Systems (ICDCS)": "https://dblp.org/db/conf/icdcs",
    "Symposium on Principles of Distributed Computing (PODC)": "https://dblp.org/db/conf/podc",
    "International Conference on Concurrency Theory (CONCUR)": "https://dblp.org/db/conf/concur",
    "Dependable Systems and Networks (DSN)": "https://dblp.org/db/conf/dsn",

    # ---------------------------------------------------
    # Computer networks
    # ---------------------------------------------------
    "Mobile Ad Hoc Networking and Computing (MobiHoc)": "https://dblp.org/db/conf/mobihoc",
    "ACM SIGCOMM Conference (SIGCOMM)": "https://dblp.org/db/conf/sigcomm",
    "Conference on Embedded Networked Sensor Systems (SenSys)": "https://dblp.org/db/conf/sensys",
    "Mobile Computing and Networking (MOBICOM)": "https://dblp.org/db/conf/mobicom",
    "International Conference on Mobile Systems (MobiSys)": "https://dblp.org/db/conf/mobisys",
    "Internet Measurement Conference (IMC)": "https://dblp.org/db/conf/imc",
    "IEEE INFOCOM": "https://dblp.org/db/conf/infocom",
    "IEEE/ACM Transactions on Networking (TON)": "https://dblp.org/db/journals/ton",
    "Ad Hoc Networks": "https://dblp.org/db/journals/adhoc",
    "International Conference on Network Protocols (ICNP)": "https://dblp.org/db/conf/icnp",
    "Computer Communication Review (CCR)": "https://dblp.org/db/journals/ccr",
    "IEEE Journal on Selected Areas in Communications (JSAC)": "https://dblp.org/db/journals/jsac",
    "IEEE Network": "https://dblp.org/db/journals/network",
    "IEEE Communications Magazine": "https://dblp.org/db/journals/commmag",
    "Sensor and Ad Hoc Communications and Networks (SECON)": "https://dblp.org/db/conf/secon",
    "Network and System Support for Games": "https://dblp.org/db/conf/netgames",
    "European Workshop on Wireless Sensor Networks": "https://dblp.org/db/conf/ewsn",
    "IEEE International Symposium on New Frontiers in Dynamic Spectrum Access Networks (DySPAN)": "https://dblp.org/db/conf/dyspan",
    "Vehicular Technology Conference (VTC)": "https://dblp.org/db/conf/vtc",
    "IEEE Wireless Communications": "https://dblp.org/db/journals/wc",
    "Network and Operating System Support for Digital Audio and Video (NOSSDAV)": "https://dblp.org/db/conf/nossdav",
    "IEEE Communications Surveys and Tutorials (COMSUR)": "https://dblp.org/db/journals/comsur",

    # ---------------------------------------------------
    # Computer security and cryptography
    # ---------------------------------------------------
    "IEEE Symposium on Security and Privacy (S&P)": "https://dblp.org/db/conf/sp",
    "ACM Conference on Computer and Communications Security (CCS)": "https://dblp.org/db/conf/ccs",
    "International Cryptology Conference (CRYPTO)": "https://dblp.org/db/conf/crypto",
    "Theory and Application of Cryptographic Techniques (EUROCRYPT)": "https://dblp.org/db/conf/eurocrypt",
    "International Conference on the Theory and Application of Cryptology and Information Security (ASIACRYPT)": "https://dblp.org/db/conf/asiacrypt",
    "Public Key Cryptography (PKC)": "https://dblp.org/db/conf/pkc",
    "Symposium on Access Control Models and Technologies (SACMAT)": "https://dblp.org/db/conf/sacmat",
    "IEEE Computer Security Foundations Workshop (CSFW)": "https://dblp.org/db/conf/csfw",
    "Network and Distributed System Security Symposium (NDSS)": "https://dblp.org/db/conf/ndss",
    "USENIX Security Symposium": "https://dblp.org/db/conf/uss",
    "iTrust": "https://dblp.org/db/conf/itrust",
    "Recent Advances in Intrusion Detection (RAID)": "https://dblp.org/db/conf/raid",
    "ACM Transactions on Information and System Security (TISSEC)": "https://dblp.org/db/journals/tissec",
    "Cryptographic Hardware and Embedded Systems (CHES)": "https://dblp.org/db/conf/ches",
    "Journal of Cryptology (JOC)": "https://dblp.org/db/journals/joc",
    "Workshop on Privacy in the Electronic Society (WPES)": "https://dblp.org/db/conf/wpes",
    "Journal of Computer Security (JCS)": "https://dblp.org/db/journals/jcs",
    "Fast Software Encryption (FSE)": "https://dblp.org/db/conf/fse",
    "IEEE Transactions on Dependable and Secure Computing (TDSC)": "https://dblp.org/db/journals/tdsc",
    "Annual Computer Security Applications Conference (ACSAC)": "https://dblp.org/db/conf/acsac",
    "Privacy Enhancing Technologies (PETS)": "https://dblp.org/db/conf/pet",
    "The Cryptographer's Track at RSA Conference (CT-RSA)": "https://dblp.org/db/conf/ctrsa",
    "Theory of Cryptography": "https://dblp.org/db/conf/tcc",

    # ---------------------------------------------------
    # Databases and data mining
    # ---------------------------------------------------
    "Conference on Innovative Data Systems Research (CIDR)": "https://dblp.org/db/conf/cidr",
    "International Conference on Management of Data (SIGMOD)": "https://dblp.org/db/conf/sigmod",
    "Very Large Data Bases (VLDB) – including The VLDB Journal": "https://dblp.org/db/conf/vldb",
    "Symposium on Principles of Database Systems (PODS)": "https://dblp.org/db/conf/pods",
    "International Conference on Database Theory (ICDT)": "https://dblp.org/db/conf/icdt",
    "Knowledge Discovery and Data Mining (KDD)": "https://dblp.org/db/conf/kdd",
    "ACM Transactions on Database Systems (TODS)": "https://dblp.org/db/journals/tods",
    "IEEE Transactions on Knowledge and Data Engineering (TKDE)": "https://dblp.org/db/journals/tkde",
    "ACM Conference on Electronic Commerce (EC)": "https://dblp.org/db/conf/ec",
    "SIAM International Conference on Data Mining (SDM)": "https://dblp.org/db/conf/sdm",
    "Sigkdd Explorations": "https://dblp.org/db/journals/sigkdd",
    "Data Mining and Knowledge Discovery (DATAMINE)": "https://dblp.org/db/journals/dmkd",
    "Journal on Data Semantics (JODS)": "https://dblp.org/db/journals/jods",
    "Distributed and Parallel Databases (DPD)": "https://dblp.org/db/journals/dpd",
    "International Workshop on the Web and Databases (WebDB)": "https://dblp.org/db/conf/webdb",
    "Sigmod Record": "https://dblp.org/db/journals/sigmod-record",
    "Information & Management": "https://dblp.org/db/journals/im",
    "Information Systems Journal (ISJ)": "https://dblp.org/db/journals/isj",
    "Information Systems Research (ISR)": "https://dblp.org/db/journals/isr",
    "Journal of Management Information Systems (J MANAGE INFORM SYST)": "https://dblp.org/db/journals/jmis",
    "Information and Organization": "https://dblp.org/db/journals/iando",
    "International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR)": "https://dblp.org/db/conf/sigir",
    "ACM Transactions on Information Systems (TOIS)": "https://dblp.org/db/journals/tois",
    "Information Research (IR)": "https://dblp.org/db/journals/ires/",
}
