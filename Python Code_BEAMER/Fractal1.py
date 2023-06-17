# Python file exported with BEAMER Revision Number 5.9.0 (35011), Dec 18 2019
# exported at 2023-Jun-05 22:25:38

# load necessary system libraries
import os
import sys

# set the path to the BEAMER python interface libraries
sys.path.append("/usr/local/BEAMER/5.9.0/lib")

import BEAMERpy

# load the python BEAMER object
BEAMER = BEAMERpy.GBEAMER()

# set the PSF Archive Directories
BEAMER.set_psf_archive_folder({ 'ArchivePath' : '/usr/local/BEAMER/5.9.0/bin/2D.Archive'})

try :
    gobj_1 = BEAMER.import_gds( { 'LayerSet' : '*', 'ImportZeroWidthPaths' : False, 'LineWidth' : 0.000000, 'ImportBoxes' : True, 'KeepElementOrder' : False, 'FlattenLayout' : False, 'LoadTextElements' : False, 'ConvertTextElementsToPolys' : False, 'ConvertedTextSize' : 1.000000, 'FileName' : '/home/benal017/patterns/Fractal_Curve_Res_Lg1.gds' } )
    gobj_2 = BEAMER.heal( gobj_1, { 'TargetLayer' : '1(0)', 'SoftFrame' : 0.300000, 'HierarchicalProcessing' : True, 'LayerAssignment' : 'AllLayer', 'ProcessingMode' : 'Healing' } )
    gobj_3 = BEAMER.pec( gobj_2, { 'UserdefinedDoseClassFile' : '**filename**', 'MinFractureSizeMode' : 'Automatic', 'BeamSize' : 0.010000, 'DoseClassMode' : 'Accuracy', 'MaxNumOfDoseClasses' : 256, 'Accuracy' : 1.000000, 'UserDefinedSeparationValue' : False, 'SeparationValue' : 0.100000, 'FractureGrid' : 0.010000, 'MinFractureSize' : 0.100000, 'MinFractureSizeShortRange' : 0.100000, 'MinDoseFactor' : 0.100000, 'MaxDoseFactor' : 10.000000, 'LayerListForCorrection' : '*', 'LayerListForFullCorrection' : '*', 'LayerForFracture' : '*', 'ContrastPartofLRPEC' : 100.000000, 'PSFFileName' : '', 'OverdoseFactor' : 1.000000, 'PSFType' : 'Archive', 'MidRangeActivationThreshold' : 2.000000, 'SingleLineBeamWidth' : 0.000000, 'IncludeSRCorrection' : False, 'HierarchicShortRangePEC' : True, 'HierarchicLongRangePEC' : False, 'ConvergenceOutput' : False, 'IncludeLateralDevelopment' : False, 'LateralDevelopmentGrid' : 0.100000, 'PSFArchiveIdentifierString' : 'Substrate_Si_Thickness_700000_Energy_100_Layers__Resist_PMMA 100 nm_Z-Position_0.045_Electrons_2000000_Alpha_0_Beta_0_Eta_0_Gamma1_0_Nue1_0_Gamma2_0_Nue2_0_Simulator_mcTrace 1.0.0', 'CellsToKeep' : '', 'Use2dLateralDevelopmentBias' : False } )
    gobj_4 = BEAMER.export_gpf( gobj_3, { 'FileName' : '/home/benal017/patterns/Fractal_Curve_Res_Lg1.gpf', 'ExtentMode' : 'Default', 'LowerLeftX' : 0.000000, 'LowerLeftY' : 0.000000, 'UpperRightX' : 0.000000, 'UpperRightY' : 0.000000, 'FormatType' : '5200 / 5000+ 20bit HS UPG 100kV', 'GridResolution' : 0.020000000000, 'BeamStepSize' : 0.020000000000, 'MainFieldResolution' : 0.000500000000, 'SubFieldResolution' : 0.000500000000, 'MainfieldSizeX' : 520.000000, 'MainfieldSizeY' : 520.000000, 'SubfieldSizeX' : 4.520000, 'SubfieldSizeY' : 4.520000, 'FractureMode' : 'LRFT', 'SymmetricFracturing' : False, 'ShotFillingMode' : 'StandardMode', 'YTrapezoids' : True, 'SequenceFile' : '', 'MainfieldPlacement' : 'Fixed', 'FixedFieldTraversal' : 'MeanderX', 'FeatureOrderingType' : 'ArrayCompaction', 'ParallelogramCompaction' : True, 'SortedOrderLayer' : '*', 'CompactionRegionSize' : 520.000000, 'RegionTraversalMode' : 'MeanderX', 'DoseOrderingType' : 'AscendingDose', 'FieldScaling' : False, 'FieldScalingLayer' : '*', 'NormalizeToOne' : False, 'TrapezoidDensityCorrection' : False, 'XScaling' : 1.000000, 'YScaling' : 1.000000, 'FieldOverlapBehaviour' : 'KeepFieldSize', 'FieldOverlapX' : 0.000000, 'FieldOverlapY' : 0.000000, 'OverlapMethod' : 'Share between Fields', 'MultipassMode' : 'Single Pass' } )
except BEAMERpy.GError as e :
    print("exception caught")
    print(e)
