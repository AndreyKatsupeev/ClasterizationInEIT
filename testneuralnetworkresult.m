clear -v
n_elec=16;
kek=load ('D:/Katsupeev/NeuroClass/result.dat');#path to results
#load ('/mnt/Disk-D/Katsupeev/NeuroClass/new/fornn_apnea2_filtered1.dat');
try imdl=mk_common_model('d2t2',n_elec);
   catch 
    run ('')#path to eidors startup.m
    end_try_catch
imdl.fwd_model.electrode =imdl.fwd_model.electrode( [(n_elec/2+1):n_elec,1:(n_elec/2)]);
[stim, meas_select] = mk_stim_patterns(n_elec,1,'{ad}','{ad}',{'no_meas_current'},5);

imdl.inv_solve.calc_solution_error = 0;
imdl.fwd_model.stimulation = stim;
imdl.fwd_model.meas_select=meas_select;
img=inv_solve(imdl,ones(208,1),ones(208,1));
img.calc_colours.ref_level=0;#;
#img.calc_colours.clim=0.02;
img.calc_colours.cmap_type = 'draeger-2009';
#img.elem_data=file.elem_data.filtered2;
img.elem_data=kek;
ind0=find(img.elem_data==0);
ind1=find(img.elem_data==1);
ind2=find(img.elem_data==2);

#img.elem_data(ind0)=1;
img.elem_data(ind2)=1;
img.elem_data(ind1)=-1;

show_fem(img,[1,1,0])
#show_slices(img);
