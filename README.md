Copyright 2014, Bryan Cort (cort@haskins.yale.edu), all rights reserved.
#####################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
#####################################################################

This is a python-executable directory including gen_mvm.py and all
dependencies from the haskins package
(https://github.com/bryancort/haskins), cloned 1-21-15.

This tool builds the 3dMVM command and associated data table. It requires
three tab separated files specifying, respectively, the within subjects
component of the design, the between subjects component of the design,
and the GLTs to include in the MVM. In addition to these files, it requires
the path to the directory containing your mri scans and the the 'tag' for
the subdirectory containing your processed data within each scan directory.
This tag is a substring that uniquely identifies the subdirectory containing
your processed data; gen_mvm will search each scan directory for a
subdirectory matching the pattern *tag*.

Optionally, you may also provide a voxelwise covariate name and pattern
(the vox_covar and vox_covar_pattern options). The name is descriptive only, 
but the pattern must match a single .HEAD or nifti file in each processed 
data subdirectory. NB: if your voxelwise covariate is in afni (head/brik)
format, be sure to include .HEAD in your vox_covar_pattern argument.

Non-voxelwise quantitative covariates must be specified with the -quant_covars
argument (and optionally centered with the -quant_covars_centers argument) as
well as included in the between subjects specfication file (see below for example).

Other options control the output location and the naming of gen_mvm's output.

Design and GLT specification details

Examples provided here are taken from an experimental design with three within
subjects factors (language, modality, and lexicality) with two levels each:
English/Hebrew for languange, Print/Speech for modality, and Word/Psuedoword
for lexicality. The design also has one between subjects variable, Site, with
two levels: NY/HU.


Within subjects design specification should be a tab-separated text file
specifying the sub-brick for each combination of within subject variables.
eg.:

Lang	Mod	Lex	subBrick
Eng	Speech	Word	1
Eng	Speech	PsWord	4
Eng	Print	Word	10
Eng	Print	PsWord	13
Heb	Speech	Word	19
Heb	Speech	PsWord	22
Heb	Print	Word	28
Heb	Print	PsWord	31


Between subjects design specification should be a tab-separated text file with
a column for subject ids (must be first and named Subj) and a column for each
between subjects variable (named as you want to see them called in the model).
There must exist directories in mri_dir containing scan data for each subject
and the directory names must match the ids in the Subj column.
eg.:

Subj	Site    covar_1
ss_1	HU      val_1
ss_2	HU      val_2
ss_3	NY      val_3
ss_4	NY      val_4
.       .       .
.       .       .
.       .       .
ss_n	site_n  val_n

NB: Subject directories in mri_dir must match these subject IDs in the Subj column;
so for this between subjects specification, there must be directories named ss_1,
ss_2, ss_3, ss_4, ... ss_n in mri_dir


GLT specification should be a text file (NOT tab separated) with the full
text of your glt specifications, eg:

-gltLabel 1 NY:ENG:PRINT:WORD -gltCode 1 'Site : 1*NY Lang : 1*Eng Mod : 1*Print Lex : 1*Word' \
-gltLabel 2 NY:HEB:PRINT:WORD -gltCode 2 'Site : 1*NY Lang : 1*Heb Mod : 1*Print Lex : 1*Word' \
-gltLabel 3 HU:ENG:PRINT:WORD -gltCode 3 'Site : 1*HU Lang : 1*Eng Mod : 1*Print Lex : 1*Word' \
.
.
.
-gltLabel N NY-HU:HEB:PRINT:WORD -gltCode N 'Site : 1*NY -1*HU Lang : 1*Heb Mod : 1*Print Lex : 1*Word' \
