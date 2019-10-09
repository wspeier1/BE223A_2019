DBSleads = load('Electrode_Locations/Mahsa_Localization/DBS_electrodes.mat');
Fiducials = load('Electrode_Locations/Mahsa_Localization/PinTips.mat');

elecmatrix= vertcat(Fiducials.elecmatrix,DBSleads.elecmatrix);
save('Electrode_Locations/Mahsa_Localization/combinedtips_dbsleads.mat','elecmatrix')

