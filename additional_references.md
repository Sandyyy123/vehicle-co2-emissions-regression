# Additional References - Project #5 CO2 Emissions

Independent literature scout, scope 2024-2026. Every entry below was verified live against `https://api.crossref.org/works/{doi}` on 2026-05-08. Not-resolving items were dropped, never padded.

Citation format: `Author1, Author2, ... Title. Journal. Year. DOI:10.xxx/yyy`. No volume, no issue, no pages.

---

## State-of-the-art callout: gaps in the current `references.md`

After completing the independent search above, a final cross-check against the existing `manuscripts/references.md` surfaces five concrete gaps the project should close before final submission:

1. **Modern tabular foundation models.** TabPFN (Hollmann et al., Nature 2025, DOI:10.1038/s41586-024-08328-6) is the first published tabular foundation model that frequently matches or beats tuned XGBoost on small-to-medium regression tasks (n < 50,000), exactly the ADEME carlab regime. The current references list none of TabPFN, FT-Transformer, SAINT, or related architectures.
2. **2024-2026 tabular benchmarks beyond Grinsztajn 2022.** The current ref [8] (Grinsztajn 2022) is the only post-2020 anchor for the "tree-based wins on tabular" claim. The Somvanshi 2026 ACM Computing Surveys piece and the Borisov IEEE TNNLS 2024 survey update that landscape and should be cited in Methods.
3. **Recent vehicle-CO2 ML application papers.** The Yuan et al. 2025 Energies paper (DOI:10.3390/en18205408) and the Yin et al. 2024 and Ji et al. 2024 papers in Transportation Research Part D are direct methodological neighbours and were published after the cited Udoh 2024 reference.
4. **Real-world PHEV CO2 data 2024-2026.** The current PHEV anchor (Tansini et al. 2022, ref [27]) predates the 2024-2026 wave of European on-board fuel-consumption monitoring (OBFCM) datasets. Mądziel and Campisi 2026 (DOI:10.3390/en19051165) and Hamza et al. 2024 (DOI:10.3390/wevj15100458) are the new canonical references and directly relevant to the manuscript's PHEV-blind-spot footnote.
5. **Methodological hygiene on leakage.** The manuscript's central diagnostic claim is that the consumption-to-CO2 link is a leakage path. None of the current references in `references.md` cite a leakage-methodology paper. Bouke et al. 2024 (DOI:10.21203/rs.3.rs-4579465/v1, preprint, omitted below for verifiability) and Apicella et al. 2024 are domain-agnostic anchors; in the verified set, the Sahin 2025 Ocean Engineering paper provides a parallel domain example of declared-consumption-driven CO2 prediction with explicit leakage discussion.

---

## Tabular ML methodology (2024-2026)

Hollmann N, Müller S, Purucker L, Krishnakumar A, Körfer M, Hoo S. Accurate predictions on small data with a tabular foundation model. Nature. 2025. DOI:10.1038/s41586-024-08328-6

Helli K, Hollmann N, Hutter F, Müller S, Schnurr D. Drift-Resilient TabPFN: In-Context Learning Temporal Distribution Shifts on Tabular Data. Advances in Neural Information Processing Systems 37. 2024. DOI:10.52202/079017-3134

Somvanshi S, Das S, Javed S, Antariksa G, Hossain A. A Survey on Tabular Data: From Tree-based Methods to Tabular Deep Learning. ACM Computing Surveys. 2026. DOI:10.1145/3807777

Borisov V, Leemann T, Sessler K, Haug J, Pawelczyk M, Kasneci G. Deep Neural Networks and Tabular Data: A Survey. IEEE Transactions on Neural Networks and Learning Systems. 2024. DOI:10.1109/tnnls.2022.3229161

Clerici F, Nobani N. Categorical variable encoding methods for tabular data: a benchmarking study. International Journal of Data Science and Analytics. 2026. DOI:10.1007/s41060-025-00886-w

---

## Vehicle CO2 prediction with ML (2024-2026)

Yuan D, Tang L, Yang X, Xu F, Liu K. Explainable Machine Learning Prediction of Vehicle CO2 Emissions for Sustainable Energy and Transport. Energies. 2025. DOI:10.3390/en18205408

Udoh J, Lu J, Xu Q. Application of Machine Learning to Predict CO2 Emissions in Light-Duty Vehicles. Sensors. 2024. DOI:10.3390/s24248219

Sahin V. Explainable machine learning-based prediction of CO2 emissions from passenger vessels. Ocean Engineering. 2025. DOI:10.1016/j.oceaneng.2025.122752

Zhu B, Hu S, Chen X, Roncoli C, Lee D. Uncovering driving factors and spatiotemporal patterns of urban passenger car CO2 emissions: A case study in Hangzhou, China. Applied Energy. 2024. DOI:10.1016/j.apenergy.2024.124094

Liu X, Guo T. Development of a Deep Learning-Based Model for Dynamic Monitoring and Analysis of Vehicle on-Road CO2 Emissions. 2025 5th International Conference on Sensors and Information Technology. 2025. DOI:10.1109/icsi64877.2025.11009944

---

## Road-transport emissions ML at fleet and urban scale (2024)

Yin C, Wu J, Sun X, Meng Z, Lee C. Road transportation emission prediction and policy formulation: Machine learning model analysis. Transportation Research Part D: Transport and Environment. 2024. DOI:10.1016/j.trd.2024.104390

Ji T, Li K, Sun Q, Duan Z. Urban transport emission prediction analysis through machine learning and deep learning techniques. Transportation Research Part D: Transport and Environment. 2024. DOI:10.1016/j.trd.2024.104389

Wang X, Qiu Z, Liu Z. Urban road BC emissions of LDGVs: Machine learning models using OBD/PEMS data. Chemosphere. 2024. DOI:10.1016/j.chemosphere.2024.143348

Pandey A, Pandey G, Mishra R. Evaluating exhaust emissions from heterogeneous car fleet through real-time field-generated dataset. Atmospheric Pollution Research. 2024. DOI:10.1016/j.apr.2024.102232

Pandey A, Pandey G, Mishra R. Emission performance evaluation of urban passenger car fleet through field investigation data in a megacity. Environmental Science and Pollution Research. 2024. DOI:10.1007/s11356-024-32555-z

Kawsar S, Biswas S, Noor M, Mamun M. Investigating the applicability of COPERT 5.5 emission software in Bangladesh and developing countrywide vehicular emission inventories. Environmental Science: Atmospheres. 2024. DOI:10.1039/d3ea00047h

---

## Real-world driving cycle and PHEV CO2 (2024-2026)

Madziel M, Campisi T. Real-World CO2 Emissions of Plug-In Hybrid Vehicles: European Assessment Using On-Board Fuel Consumption Monitoring Data. Energies. 2026. DOI:10.3390/en19051165

Hamza K, Laberteaux K, Chu K. An Approach for Estimating the Contributions of Various Real-World Usage Conditions towards the Attained Utility Factor of Plug-In Hybrid Electric Vehicles. World Electric Vehicle Journal. 2024. DOI:10.3390/wevj15100458

Hamza K, Laberteaux K, Chu K. An Approach for Estimating Contributions of Real-World Factors towards Attained Well-to-Wheels Greenhouse Gas Emissions of Plug-in Hybrid Electric Vehicles. SAE International Journal of Advances and Current Practices in Mobility. 2025. DOI:10.4271/2025-01-8543

Jeong J, Lee G, Lee J, Woo S, Kim N, Lee K. Analysis of energy consumption and emissions characteristics of plug-in hybrid electric vehicle (PHEV) under various real-world driving conditions. Journal of Environmental Sciences. 2026. DOI:10.1016/j.jes.2025.11.033

Nitoiu C, Cofaru C, Popescu M. Influence of road and traffic conditions on emissions and fuel consumption of light vehicles in a real urban driving cycle. Environmental Science and Pollution Research. 2025. DOI:10.1007/s11356-025-36573-3

---

## EU passenger-car policy and fleet trajectories (2024-2025)

Nguyen T, Hirz M. Effects of automated cars on CO2-equivalent emissions of European passenger car fleet: a life cycle perspective. Transportation Research Procedia. 2025. DOI:10.1016/j.trpro.2025.04.045

Chatti W, Majeed M, Khoj H, Miraz M, Ali A. Towards smart and sustainable transportation: the role of artificial intelligence and new technologies in mitigating passenger car CO2 emissions. Environment, Development and Sustainability. 2024. DOI:10.1007/s10668-024-05685-0

---

## Notes on omitted candidates

- Several SSRN preprints surfaced strong title matches (e.g. "CO2 Emissions Prediction from Urban Commuting Using XGBoost and SHAP", DOI:10.2139/ssrn.6685381) but resolved to `null` publication year on CrossRef and were dropped to avoid pre-print padding.
- Pre-print archives (ResearchSquare, TechRxiv, ESSOAR) were excluded unless the underlying journal version had been issued and indexed.
- All entries above were re-verified individually via `api.crossref.org/works/{doi}` and returned HTTP 200 with matching title strings.
