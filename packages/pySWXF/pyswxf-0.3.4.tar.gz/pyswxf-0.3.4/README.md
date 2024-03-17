# pySWXF 

Code for calculating reflectivity and standing wave x-ray reflectivity


## get_prof  Routine to get electron density profile from list of amplitudes centers and roughnesses
	* get_prof:		Gets profile
	* get_dprof:		Gets profile derivative
## get_realspace	Routine to get realspace profile for bilayer.  Probably obselete
	* get_realspace 
	* half	routine to do a 1/2 boxcar average of data set and halve length of dataset 

## refl_funs  Routines to calculate specular reflectivity
	* mlayer_rough:		Calculates reflectivity from a multilayer substrate.  Approximates roughness as gaussian
	* mlayer_conv		Convolutes mlayer_rough with a gaussian resolution function

## spec_utils  Routines to read data from spec files
	* readscan		read a data scan
	* readmcascan		read a data scan where mca data saved to spec file 
	* merge_scans		combine spec scans from a sequence
	* merge_duplicates	take combined scans and average points at same location
	* getscan			uses readscan to specifically read theta two-theta data
	* getscan_bg		reads a scan and two backgrounds and returns background subtracted data
	* list_scans		lists scans in spec file
		* dt_correct:		corrects MCA dead time from CLS mca
	* get_mca_data_CLS: 	reads MCA data from Canadian Light Source Brockhouse Beamline
	* get_mca_data_DND:	reads MCA data from DND cat
	* plot_mca_sum:		Sums all mca data from a scan and plots intensity vs energy 
	* peak_label:		Plots a label for a peak on an MCA plot
	* K_label:		Labels all K-lines from an element
	* L_label:		Labels all L-lines from an element
	* get_br_amps		Fits bromine peak to gaussian and nearby gold peak.  Returns only Br amplitude
	* plot_br_fluor		Fits all bromine amplitudes from scan and returns plot of intensity vs. angle
	* get_edge_absorb		Finds the absorbtion probability of an edge by brute force (e.g. 
					calculates values on either side of edge and subtracts
	* Au_L_peak:		Simulates intensity from Au L peaks.  Input to get_br_amps
	* Br_K_peak:		Simulates intensity from Br K peak.  Input to get_br_amps
	* Br_peak_sim:		Combines Br and Au peaks into total intensity.  Input to get_br_amps
		* cbwe: combine two sets of data with error bars
	* cbwe_s: same as cbwe but for two scalers rather than two vector
	* get_reflectivity_CLS(fname, datadir, scan):
	* get_refl_sequence_CLS(fname, datadir, firstscan):
	* plot_refl_sequence_CLS(fname, datadir, firstscan):

## standing_wave	Routines to calculate x-ray standing wave properties
	* reflection_matrix 	returns reflection and transmission data from multilayer array.  Uses mlayer_rough
	* eden_to_rho		converts between electron density and mass density
	* rho_to_n		converts between mass density and index of refraction
	* rho_to_rhoe		converts between mass density and electron density


Some of these are still a work in progress, proceed with caution

Please contact Larry Lurio llurio@niu.edu for more information

