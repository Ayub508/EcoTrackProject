# Problem Definition

## 1. Context

Climate change remains one of the most pressing global challenges, and individual carbon footprint awareness is increasingly recognised as a component of broader mitigation strategies. A growing number of mobile applications — including Giki Zero, MyCarbon, and EarthHero — aim to help users estimate and reduce their personal carbon emissions. However, existing tools exhibit significant limitations in three key areas: transparency of emission factors, accuracy of calculations, and behavioural support for sustained change.

## 2. Limitations of Existing Applications

### 2.1 Limited Transparency in Emission Factors

Carbon footprint calculators rely on emission factors — numerical coefficients that convert activity data (e.g., kilometres driven, kWh consumed) into CO2-equivalent estimates. A review published in *ScienceDirect* found that there is "little uniformity or transparency across the various tools" used for personal carbon calculation (Shaikh et al., 2025). Providers use different data collection methods and offer varying levels of transparency in their reporting processes, leading to differences in data quality that impact reliability (Climatiq, 2024). None of the three applications examined — Giki Zero, MyCarbon, or EarthHero — publicly document the specific emission factor databases or conversion methodologies underpinning their estimates. Users are therefore unable to verify, interrogate, or compare the basis of their results.

### 2.2 Low Accuracy of Carbon Estimates

Research from Carnegie Mellon University demonstrated that "the calculation of carbon footprints for products is often riddled with large uncertainties," with variables from production, shipping, and manufacturing technology all altering accuracy (ScienceDaily, 2010). These inaccuracies are reflected in consumer-facing tools:

- **Giki Zero** initially produces a broad estimate from a small number of lifestyle questions. Accuracy improves only when users manually input detailed data across multiple categories, a process the platform itself acknowledges requires sustained time and commitment.
- **EarthHero** estimates the footprint of material consumption based on spending amounts rather than specific product-level data, which the app's own review coverage describes as "a bit misleading — especially as most sustainable options are more expensive" (Earthplex, 2021). The application's terms of service explicitly state that Earth Hero "does not warrant against nor accepts legal responsibility for the accuracy, completeness, or usefulness of any data."
- **MyCarbon** automatically detects transport mode and distance, but its scope is limited primarily to travel emissions, leaving large emission categories (diet, housing, consumption) unaddressed or estimated at a coarse level.

Discrepancies between calculators are also well-documented. Different tools apply different system boundaries — some divide national emissions per capita, while others count only directly attributable activities — leading to inconsistent results for the same user (Padgett et al., 2008).

### 2.3 Weak Behavioural Support

Sustained behavioural change requires more than awareness. The Motivation-Ability-Opportunity (MAO) framework, as applied by Livework Studio (2022), identifies that most carbon tracking apps focus disproportionately on motivation (e.g., showing users their footprint) while neglecting ability (knowledge and financial resources to act) and opportunity (access to infrastructure, alternatives, and supportive social contexts).

Specific shortcomings include:

- **Giki Zero** provides action suggestions but offers limited support for users who lack the financial resources or practical knowledge to implement them.
- **EarthHero** provides sustainability recommendations with difficulty ratings but does not adapt to the user's context, location, or constraints. Much of its advice is US-centric, limiting relevance for users in other regions.
- **MyCarbon** offers carbon offset purchases through 20+ global projects, but offsets have been widely criticised — a systematic review of over 100 studies declared carbon offsets "largely ineffective" as a behavioural intervention (Imagine5, 2023).

None of these applications integrate collective action mechanisms, goal-setting frameworks with adaptive feedback, or context-aware recommendations that account for individual circumstances.

## 3. The Gap

There is a demonstrable gap in the current landscape of personal carbon tracking tools. Existing applications suffer from:

1. **Opaque methodologies** — emission factors and calculation boundaries are not disclosed, preventing user trust and academic scrutiny.
2. **Inaccurate or coarse estimates** — reliance on spending proxies, limited input categories, or national averages produces results with significant uncertainty.
3. **Insufficient behavioural design** — a narrow focus on individual motivation without addressing ability and opportunity leads to low sustained engagement and minimal real-world impact.

## 4. Proposed Response

EcoTrack addresses this gap by providing a personal carbon footprint tracking system that prioritises:

- **Transparent emission factors** — all conversion coefficients are documented with source references, enabling users and reviewers to trace any estimate back to its underlying data.
- **Granular, evidence-based calculations** — footprint estimates are derived from specific activity inputs across all major emission categories (transport, energy, diet, consumption), reducing reliance on spending-based proxies or national averages.
- **Behaviourally-informed support** — recommendations are structured around the MAO framework, addressing not only what users should change but how they can realistically do so given their individual context, with adaptive goal-setting and progress tracking.

This system is designed to improve upon the identified limitations of existing tools and to contribute to the evidence base on effective personal carbon management applications.

---

## References

- Climatiq (2024) *Establishing the Standard for Emission Factor Data*. Available at: https://www.climatiq.io/blog/emission-factor-data-standard
- Earthplex (2021) *Earth Hero: Can This App Lower Emissions?* Available at: https://www.earthplexmedia.com/2021/01/earth-hero-app-impressions.html
- Livework Studio (2022) *What carbon impact tracking apps are getting wrong, and how to fix it*. Available at: https://liveworkstudio.com/insight/what-carbon-impact-tracking-apps-are-getting-wrong-and-how-to-fix-it/
- Padgett, J.P. et al. (2008) 'A comparison of carbon calculators', *Environmental Impact Assessment Review*, 28(2-3), pp. 106-115.
- ScienceDaily (2010) *Large uncertainty in carbon footprint calculating*. Available at: https://www.sciencedaily.com/releases/2010/12/101213121741.htm
- Shaikh, M.A. et al. (2025) 'A review and development of an enhanced carbon footprint calculator', *Journal of Cleaner Production*. Available at: https://www.sciencedirect.com/science/article/pii/S0959652625016427
