---
layout: page
title: "CRISPRi/a cell line primer"
permalink: /crispria_cell_line_primer/
---

## A primer on CRISPRi/a cell line production

**A key parameter for implementing CRISPRi/a systems is construction of cell lines
where dCas9 chimera proteins are stably and efficiently expressed in mammalian cells.
Although this statement may seem obvious it has been our experience that generating a
line where close to 100% of cells in a polyclonal or clonal population stably express
dCas9 indefinitely without lentiviral silencing is a crucial aspect of successfully
implementing CRISPRi/a systems.**

### Introduction to CRISPRi/a
CRISPR (clustered regularly interspaced short palindromic repeats), an adaptive genome
defense system in bacteria and archaea, has been widely repurposed as an RNA-guided
genome editing method. CRISPR-based editing minimally requires expression of the Cas9
endonuclease and a customizable targeting single-guide RNA (sgRNA). We showed that the
endonuclease domains of the Cas9 protein can be mutated (dead Cas9 or dCas9) to create a
programmable RNA-guided DNA-binding protein in human cells.

CRISPRi is a relatively new way to repress expression of any transcript encoded by a
mammalian genome. We have used dCas9-KRAB fusion proteins to repress transcription.
This activity is enacted in part through dCas9’s ability to block elongating RNA polymerase
to directly repress gene expression and in part through the KRAB domain which is a general
transcription repressor that recruits KAP1, HP1α and other proteins to edit the epigenome and
silence transcription locally. We have shown we can repress both coding and non-coding
genes. With properly designed reagents this method is highly specific and highly active.
CRISPRa is a new way to activate expression of transcripts encoded by mammalian genomes.
We have implemented CRISPRa systems initially by fusing strong viral transcription
activation domains directly to dCas9, and then improved upon this by creating the “SunTag”
system which uses dCas9 chimeras to recruit 10 transcription activation domains.

We have designed a series of first and second generation genome scale libraries for CRISPRi
and CRISPRa enabling loss- and gain-of-function functional genomic screens (PUBMED: V2
design: 27661255, V1 design (discontinued on Addgene): 25307932). The V2 human and
mouse genome scale libraries (Addgene: https://www.addgene.org/browse/article/22413/) are
available through Addgene and are in all ways we have tested superior to the V1 library,
which we now consider obsolite. The sgRNAs present in these libraries also represent our
best predictions for sgRNA sequences that are highly active for repressing or activating gene
expression, see the supplementary tables of the relevant papers for sgRNA sequences. We
have deposited our standard sgRNA expression vector on Addgene. We strongly recommend
that users follow our optimized sgRNA constant region design which differs from the design
many other labs use and confers higher guides expression and stability (PUBMED: 24360272,
25307932 and available on Addgene: 60955).

### CRISPRi cell line production

#### Which CRISPRi vector should I use? 
We have cloned a panel of CRISPRi lentiviral vectors with different promoters and
anti-silencing DNA elements. One or more than one of these vectors has been implemented to
stably express dCas9 chimeras in the cell lines we have tested to date. Promoter activity and
silencing is variable between cell lines likely reflecting the developmental status and
transcriptional logic of each cell line. We use the 5 vectors listed below most frequently.
- SFFV-dCas9-BFP-KRAB (Addgene: 46911)
- EF1α-dCas9-BFP-KRAB (Addgene: Available soon)
- UCOE-SFFV-dCas9-KRAB (Addgene: Available soon)
- UCOE- EF1α-dCas9-BFP-KRAB (Addgene: Available soon)
- TRE3G-KRAB-dCas9-P2A-mCherry (Available soon or subclone TRE3G promoter into Addgene: 60954)

The SFFV promoter is a strong viral promoter but can be silenced in certain cell types. The
SFFV promoter has one crucial advantage in that it is only ~500bp keeping lentiviral titers
high. The EF1α promoter is more broadly useful but is ~1500bp and so lenti titers are lower
for these constructs. We have found, as is previously reported (PUBMED: 20588258 and
25605798), that **incorporating a ubiquitous chromatin opening element (UCOE)
upstream of the promoter prevents silencing of integrated lentiviral dCas9 constructs in
various cell types.** We have found **the UCOE constructs to be extremely useful for
generating cell lines that have robust and stable expression of the dCas9 chimera
expression, and now recommend these constructs as the first vectors to try for any user
intending to establish a new constitutive CRISPRi cell line.**

#### Should I use an inducible or constitutive CRISPRi system?
Constitutive and inducible CRISPRi systems are both useful and you should tailor the system
to your experimental needs. We generally use constitutive systems unless there is a specific
biological or technical reason to use an inducible system as the inducible systems are more
complex to implement. To implement our inducible CRISPRi system requires constitutive
expression of the tet3G protein (separate plasmid available through Clontech) and inducible
expression of dCas9-KRAB (TRE3G vector listed above). Although inducible systems are
highly attractive it is not always trivial to generate a cell line with minimally leaky CRISPRi
activity and strong, stable, homogenous induction of dCas9-KRAB expression upon addition
of doxycycline.

#### How do I construct a CRISPRi cell line?
To construct a polyclonal CRISPRi line, we generate lentivirus as described below and then
infect a population of cells with one of the CRISPRi constructs listed above at ~30-70%
infection rate. We expand the infected cells for 3-5 days and then use flow cytometry to sort a
100% pure population of cells expressing dCas9-KRAB. We generally sort the top half of the
BFP positive cells by BFP signal intensity. We have also infected cells at high multiplicity of
infection where 100% of cells are infected thereby ensuring each cell expresses dCas9-KRAB
or infect and then generate cell clones if sorting is not feasible.

We have found that generally the BFP signal from these BFP-dCas9 fusions is weaker than
from monomeric BFP alone and also that in many cases BFP/dCas9 levels are tuned down by 
cells following infection over time. In some cases, higher levels of BFP correlate with better
CRISPRi activity especially if you are expressing 2 or 3 sgRNAs. However in many cases
very low BFP levels are sufficient for full CRISPRi activity and the more important
parameter is that all of the cells in the FACS sorted polyclonal population express the dCas9
chimera. We check our sorting purity on a flow cytometer immediately post sorting and if the
purity is not at least ~99.9% we re-sort 3-4 days later.

#### How do I test if my CRISPRi cell lines are highly active?
To test if your CRISPRi cell line is active and can repress transcription robustly we suggest
testing a series of positive control knockdowns by expressing positive control sgRNAs in
your newly constructed cell line and then measuring CRISPRi activity as evidenced by
knockdown of the targeted gene.

First, expand your newly generated CRISPRi cell line and freeze several vials of cells. We
then generate lentivirus for positive control sgRNAs as described below and infect the
CRISPRi cell line. The lenti sgRNA constructs co-express a puromycin resistance cassette as
well as either BFP (Addgene: 60955), GFP or mCherry. A population of infected cells can be
sorted to purity using flow cytometry or selected to purity using puromycin. We most
frequently use the dCas9-BFP-KRAB fusion together with an sgRNA lenti that co-expresses
BFP and puro markers. The BFP signal from the dCas9-BFP-KRAB fusion protein is
typically 10-20x less bright than the BFP signal from monomeric BFP co-expressed from the
sgRNA lenti vector and so these two BFP signals can be quantitatively distinguished allowing
us to reserve GFP and mCherry for downstream experiments.

To help labs test new CRISPRi cell lines, we have deposited on Addgene our published GFP
CRISPRi reporter (Addgene: 46919). The GFP reporter allows you to generate single-cell
flow cytometry data to troubleshoot and validate CRISPRi activity and cell line production.
We have included [positive control sgGFP sequences](/resources/positivecontrolsgRNAlist_V4.xlsx) to be cloned into our sgRNA expression
vector (Addgene: 60955). We have also included with this protocol a list of [positive control sgRNAs](/resources/positivecontrolsgRNAlist_V4.xlsx)
targeting human genes that have shown high activity across cell lines. We then use
qPCR to measure knockdown efficiency for this second type of positive control.

### CRISPRa cell line production
Our current gold standard CRISPRa system is the SunTag system described in PUBMED: 25307933.
This lentiviral system requires co-expression of a dCas9 fusion protein that has 10
high affinity binding sites (dCas9-10xGCN4 available on Addgene: 60903) and a single chain
variable fragment antibody that binds to the GCN4 epitope that is fused to super folder GFP
and the VP64 transcription activation domain (scFV-sfGFP-VP64 available on Addgene:
60904). To build a CRISPRa cell line we sequentially infect the dCas9-10xGCN4 fusion and
then the scFV-sfGFP-VP64. To maximize CRISPRa activity one in theory must express at
least 10x more scFV-sfGFP-VP64 than dCas9-10xGCN4 to saturate all 10 epitope binding
sites. **In practice, to generate a stable population of CRISPRa cells with the right protein
expression levels, we have found that we need to derive clonal cell lines and test
CRISPRa activity using a functional assay.**

To help labs test new CRISPRa cell lines, we have deposited on Addgene our published GFP
CRISPRa reporter (Addgene: Available soon). We have included [positive control sgRNA sequences](/resources/positivecontrolsgRNAlist_V4.xlsx)
targeting the endogenous human CXCR4 gene. Both of these positive controls can
be used to read out single cell CRISPRa activity using flow cytometry. We have also included
a [list of positive control sgRNAs](/resources/positivecontrolsgRNAlist_V4.xlsx) targeting human genes that have shown high activity. We
have used qPCR to measure gene activation efficiency for this second type of positive control.
Additional protocols and reagents are linked here:
- [Positive control sgRNAs for CRISPRi and CRISPRa](/resources/positivecontrolsgRNAlist_V4.xlsx)
- [sgRNA cloning protocol](/resources/sgRNACloningProtocol.pdf)
- [sgRNA assembly template](/resources/sgRNAAssemblyTemplate.xlsx)



### Lentivirus Production (10cm)

#### Materials:
- 10 cm plate of 293T cells (Falcon)
- 45 ul Mirus LT1 tranfection reagent
- 1500 ul Serum Free MEM or DMEM
- 8 ug of packaging vector pCMV-dR8.91
- 1 ug of packaging vector pMD2-G
- 9 ug of lentiviral plasmid

(Note this plasmid ratio is roughly a 4:1:4 molar ratio as the plasmid sizes of the
packaging vectors are pCMV-dR8.91 12150 bp, pMD2G 5824 bp, and pHR-dCas9
14000 bp)

#### Methods:

*The day before, plate 5-6 x 10^6 293T cells in 10-12 mL medium in a 10cm TC plate.*

1. In 1.5 ml tubes mix 1500ul serum free DMEM with 45 ul Mirus and incubate for 5 minutes at room temp
2. In a separate tube mix lentiviral plasmid with packaging plasmids
3. Pipette DMEM-mirus mixture into the plasmid mixture and mix vigorously
4. Incubate 30 minutes at room temperature
5. Pipette into 293T plate
6. Add 24uL Titer max to 293T plate (Stock is 500x from Alstem)
7. Allow viral production to continue for 72 hours before harvest (The medium is fairly depleated by 72hrs- I usually add 5mL fresh media 48hrs post transfection)
8. Filter supernatant through 0.4 uM filter

Scaled to single wells in a 6 well plate (9cm^2)

Plate between 600k and 1.2 million cells the day before in 3mL in each well of a 6 well plate

Transfect
- 1.35 ug of packaging vector pCMV-dR8.91
- 165 ng of packaging vector pMD2-G
- 1.5 ug of lentiviral plasmid
with 7.5uL of mirus in 300uL serum free media

#### Lentivirus Infection
Lentiviral infection parameters must be established for each cell line but the guidelines below
offer some general principles and recommendations.

For sgRNA constructs in K562 cells and most easy-to-infect adherent cell lines, we generally
add 100-200uL of fresh viral supernatant to 200,000 cells + 8ug/mL polybrene final
concentration in a total volume of 1mL in a well of a 24 well plate which results in 20-40%
infection..

Adding a “spinfection” step generally increases your infection rate but is not required. We
generally spin at 1000g for 5 minutes up to 2 hours depending on the target infection rate.

The viral titer depends on the size of the lentiviral construct. Large constructs that approach
or exceed the natural maximum HIV/lenti LTR to LTR packaging limit have low titers. Our
dCas9 fusions lenti have 3-10 fold lower titer than smaller lenti constructs like sgRNAs. Your
titer also depends on your HEK293 cell health and transfection efficiency. Do not let your
HEK293 cells get over-confluent and be sure to trypsinize well to obtain single cells!!!
Clumpy 293s produce lower titer virus.

We have also used ViralBoost from Alstem (Cat: VB100) or lentiviral concentration using
commercial precipitation (Alstem: VC100) to boost infection rates for a variety of
experiments. 