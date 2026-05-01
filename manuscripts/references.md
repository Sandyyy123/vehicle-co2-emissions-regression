# References - CO2 Emissions Prediction from Vehicle Attributes

Verified via CrossRef, Europe PMC, and arXiv (May 2026). Each reference has a resolvable DOI or arXiv ID.

## ML method foundations

1. **Breiman, L.** (2001). Random Forests. *Machine Learning*, 45(1), 5-32. DOI: [10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324). Introduces the random-forest ensemble: bagged decision trees with random feature subsetting per split, the dominant baseline for tabular regression.

2. **Friedman, J. H.** (2001). Greedy Function Approximation: A Gradient Boosting Machine. *The Annals of Statistics*, 29(5), 1189-1232. DOI: [10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451). Original gradient boosting framework; iteratively fits weak learners to functional gradients of the loss, foundation for XGBoost, LightGBM, CatBoost.

3. **Chen, T., & Guestrin, C.** (2016). XGBoost: A Scalable Tree Boosting System. *Proc. 22nd ACM SIGKDD*, 785-794. DOI: [10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785). Regularised, sparsity-aware gradient boosting with second-order Taylor expansion; de-facto standard for tabular regression benchmarks.

4. **Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A.** (2018). CatBoost: Unbiased Boosting with Categorical Features. arXiv:[1706.09516](https://arxiv.org/abs/1706.09516). Ordered boosting and target-encoded categorical handling; useful for fuel-type and body-type variables in vehicle datasets.

5. **Lundberg, S. M., & Lee, S.-I.** (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*. arXiv:[1705.07874](https://arxiv.org/abs/1705.07874). Introduces SHAP values, a Shapley-game-theoretic unification of feature-attribution methods.

6. **Lundberg, S. M., Erion, G., Chen, H., et al.** (2020). From Local Explanations to Global Understanding with Explainable AI for Trees. *Nature Machine Intelligence*, 2(1), 56-67. DOI: [10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9). Polynomial-time exact SHAP for tree ensembles; the standard interpretability tool for boosted-tree CO2 models.

7. **LeCun, Y., Bengio, Y., & Hinton, G.** (2015). Deep Learning. *Nature*, 521, 436-444. DOI: [10.1038/nature14539](https://doi.org/10.1038/nature14539). Canonical review of deep neural networks; cited when justifying or contrasting MLP regression baselines on tabular data.

8. **Grinsztajn, L., Oyallon, E., & Varoquaux, G.** (2022). Why Do Tree-Based Models Still Outperform Deep Learning on Typical Tabular Data? *NeurIPS 2022*. DOI: [10.52202/068431-0037](https://doi.org/10.52202/068431-0037). Empirical benchmark showing tree ensembles beat deep nets on tabular tasks; supports the choice of XGBoost/RF over MLPs for ADEME-style data.

## ML applied to vehicle emissions and fuel consumption

9. **Alam, G. M. I., Tanim, S. A., Sarker, S. K., et al.** (2025). Deep Learning Model Based Prediction of Vehicle CO2 Emissions with Explainable AI Integration for Sustainable Transport. *Scientific Reports*, 15. DOI: [10.1038/s41598-025-87233-y](https://doi.org/10.1038/s41598-025-87233-y). End-to-end DL pipeline with SHAP attribution for vehicle CO2 prediction, directly comparable to the ADEME task.

10. **Ibrahim, R. A., & Zakzouk, N. E.** (2026). A Machine Learning Framework for Predicting Fuel Consumption and CO2 Emissions in Hybrid and Combustion Vehicles. *PLoS ONE*. DOI: [10.1371/journal.pone.0342418](https://doi.org/10.1371/journal.pone.0342418). Compares ML regressors for joint fuel-consumption and CO2 prediction across ICE and HEV powertrains.

11. **Yoo, S. R., Shin, J. W., & Choi, S. H.** (2025). Machine Learning Vehicle Fuel Efficiency Prediction. *Scientific Reports*, 15. DOI: [10.1038/s41598-025-96999-0](https://doi.org/10.1038/s41598-025-96999-0). Tabular ML benchmark for fuel-economy prediction from vehicle technical attributes.

12. **Udoh, J., Lu, J., & Xu, Q.** (2024). Application of Machine Learning to Predict CO2 Emissions in Light-Duty Vehicles. *Sensors*, 24(24), 8219. DOI: [10.3390/s24248219](https://doi.org/10.3390/s24248219). Random-forest, GBM, and neural-net comparison on light-duty CO2 prediction.

13. **Mądziel, M.** (2025). Predictive Methods for CO2 Emissions and Energy Use in Vehicles at Intersections. *Scientific Reports*, 15. DOI: [10.1038/s41598-025-91300-9](https://doi.org/10.1038/s41598-025-91300-9). Microscopic ML emissions modelling under stop-and-go conditions; useful contrast to lab-cycle prediction.

14. **Ramirez-Sanchez, E., Tang, C., Xu, Y., et al.** (2025). NeuralMOVES: A Lightweight and Microscopic Vehicle Emission Estimation Model Based on Reverse Engineering and Surrogate Learning. arXiv:[2502.04417](https://arxiv.org/abs/2502.04417). Neural surrogate of MOVES achieving 6% MAPE at 2.4 MB; example of ML compressing physical emissions models.

15. **Beba, H., & Öztürk, Z.** (2025). Investigation of Road Transport-Based Greenhouse Gas Prediction Models and the Use of Intelligent Transportation Systems. *Scientific Reports*, 15. DOI: [10.1038/s41598-025-29724-6](https://doi.org/10.1038/s41598-025-29724-6). Survey-plus-modelling of road-transport GHG predictors at a national scale.

## Vehicle CO2 emissions: regulatory context and lab-vs-real-world gap

16. **Tietge, U., Mock, P., Franco, V., & Zacharof, N.** (2017). From Laboratory to Road: Modeling the Divergence Between Official and Real-World Fuel Consumption and CO2 Emission Values in the German Passenger Car Market for the Years 2001-2014. *Energy Policy*, 103, 212-222. DOI: [10.1016/j.enpol.2017.01.021](https://doi.org/10.1016/j.enpol.2017.01.021). Foundational ICCT study quantifying the growing 14-42% gap between NEDC type-approval and real-world CO2.

17. **Fontaras, G., Zacharof, N.-G., & Ciuffo, B.** (2017). Fuel Consumption and CO2 Emissions from Passenger Cars in Europe - Laboratory Versus Real-World Emissions. *Progress in Energy and Combustion Science*, 60, 97-131. DOI: [10.1016/j.pecs.2016.12.004](https://doi.org/10.1016/j.pecs.2016.12.004). Authoritative review of EU CO2 measurement, the lab-real gap, and engineering drivers (mass, aerodynamics, transmission).

18. **Pavlovic, J., Ciuffo, B., Fontaras, G., et al.** (2018). How Much Difference in Type-Approval CO2 Emissions from Passenger Cars in Europe Can Be Expected from Changing to the New Test Procedure (NEDC vs. WLTP)? *Transportation Research Part A*, 111, 136-147. DOI: [10.1016/j.tra.2018.02.002](https://doi.org/10.1016/j.tra.2018.02.002). Quantifies the WLTP shift and its implications for fleet CO2 targets.

19. **Tsiakmakis, S., Fontaras, G., Ciuffo, B., & Samaras, Z.** (2017). A Simulation-Based Methodology for Quantifying European Passenger Car Fleet CO2 Emissions. *Applied Energy*, 199, 447-465. DOI: [10.1016/j.apenergy.2017.04.045](https://doi.org/10.1016/j.apenergy.2017.04.045). EU-wide vehicle-attribute-driven simulation framework; methodological reference for the ADEME prediction task.

20. **Ciuffo, B., & Fontaras, G.** (2017). Models and Scientific Tools for Regulatory Purposes: The Case of CO2 Emissions from Light Duty Vehicles in Europe. *Energy Policy*, 109, 76-81. DOI: [10.1016/j.enpol.2017.06.057](https://doi.org/10.1016/j.enpol.2017.06.057). Policy-modelling overview connecting ML/simulation outputs to regulatory CO2 fleet targets.

21. **Helmers, E., Leitão, J., Tietge, U., & Butler, T.** (2019). CO2-Equivalent Emissions from European Passenger Vehicles in the Years 1995-2015 Based on Real-World Use. *Atmospheric Environment*, 198, 122-132. DOI: [10.1016/j.atmosenv.2018.10.039](https://doi.org/10.1016/j.atmosenv.2018.10.039). Real-world fleet CO2 trajectory and the climate effect of the EU diesel share.

22. **Chatzipanagi, A., Pavlovic, J., Ktistakis, M. A., Komnos, D., & Fontaras, G.** (2022). Evolution of European Light-Duty Vehicle CO2 Emissions Based on Recent Certification Datasets. *Transportation Research Part D*, 107, 103287. DOI: [10.1016/j.trd.2022.103287](https://doi.org/10.1016/j.trd.2022.103287). Recent EU certification-data analysis post-WLTP transition.

## Vehicle / automotive engineering and real-world testing

23. **Weiss, M., Irrgang, L., Kiefer, A. T., Roth, J. R., & Helmers, E.** (2020). Mass- and Power-Related Efficiency Trade-Offs and CO2 Emissions of Compact Passenger Cars. *Journal of Cleaner Production*, 243, 118326. DOI: [10.1016/j.jclepro.2019.118326](https://doi.org/10.1016/j.jclepro.2019.118326). Empirical mass/power CO2 elasticities, directly relevant for feature-importance interpretation.

24. **Suarez, J., Makridis, M., Anesiadou, A., et al.** (2022). Benchmarking the Driver Acceleration Impact on Vehicle Energy Consumption and CO2 Emissions. *Transportation Research Part D*, 107, 103282. DOI: [10.1016/j.trd.2022.103282](https://doi.org/10.1016/j.trd.2022.103282). Quantifies driving-style effects beyond technical-attribute predictors.

25. **Suarez-Bertoa, R., Valverde, V., Clairotte, M., et al.** (2019). On-Road Emissions of Passenger Cars Beyond the Boundary Conditions of the Real-Driving Emissions Test. *Environmental Research*, 176, 108572. DOI: [10.1016/j.envres.2019.108572](https://doi.org/10.1016/j.envres.2019.108572). PEMS data showing CO2 sensitivity to ambient conditions outside RDE windows.

26. **Chen, K., Zhao, F., Liu, X., Hao, H., & Liu, Z.** (2021). Impacts of the New Worldwide Light-Duty Test Procedure on Technology Effectiveness and China's Passenger Vehicle Fuel Consumption Regulations. *IJERPH*, 18(6), 3199. DOI: [10.3390/ijerph18063199](https://doi.org/10.3390/ijerph18063199). Cross-jurisdictional WLTP impact analysis on technology effectiveness ratings.

## Hybrid and electric vehicle CO2 modelling

27. **Tansini, A., Pavlovic, J., & Fontaras, G.** (2022). Quantifying the Real-World CO2 Emissions and Energy Consumption of Modern Plug-in Hybrid Vehicles. *Journal of Cleaner Production*, 362, 132191. DOI: [10.1016/j.jclepro.2022.132191](https://doi.org/10.1016/j.jclepro.2022.132191). Real-world PHEV CO2 measurement; key for any model that includes hybrid powertrains as a fuel-type level.

28. **Smith, E., Woody, M., Wallington, T. J., et al.** (2025). Greenhouse Gas Reductions Driven by Vehicle Electrification Across Powertrains, Classes, Locations, and Use Patterns. *Environmental Science & Technology*. DOI: [10.1021/acs.est.5c05406](https://doi.org/10.1021/acs.est.5c05406). Use-pattern-aware GHG accounting across BEV, HEV, ICE.

29. **Šimaitis, J., Lupton, R., Vagg, C., et al.** (2025). Battery Electric Vehicles Show the Lowest Carbon Footprints Among Passenger Cars Across 1.5-3.0 °C Energy Decarbonisation Pathways. *Communications Earth & Environment*, 6. DOI: [10.1038/s43247-025-02447-2](https://doi.org/10.1038/s43247-025-02447-2). Lifecycle CO2 across BEV vs ICE under multiple grid-decarbonisation scenarios.
