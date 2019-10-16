
function varargout = MRI_Fid_Localizer(varargin)
% MRI_FID_LOCALIZER MATLAB code for MRI_Fid_Localizer.fig
%      MRI_FID_LOCALIZER, by itself, creates a new MRI_FID_LOCALIZER or raises the existing
%      singleton*.
%
%      H = MRI_FID_LOCALIZER returns the handle to a new MRI_FID_LOCALIZER or the handle to
%      the existing singleton*.
%
%      MRI_FID_LOCALIZER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in MRI_FID_LOCALIZER.M with the given input arguments.
%
%      MRI_FID_LOCALIZER('Property','Value',...) creates a new MRI_FID_LOCALIZER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before MRI_Fid_Localizer_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to MRI_Fid_Localizer_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help MRI_Fid_Localizer

% Last Modified by GUIDE v2.5 02-Mar-2015 15:06:59

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @MRI_Fid_Localizer_OpeningFcn, ...
                   'gui_OutputFcn',  @MRI_Fid_Localizer_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before MRI_Fid_Localizer is made visible.
function MRI_Fid_Localizer_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to MRI_Fid_Localizer (see VARARGIN)

% Choose default command line output for MRI_Fid_Localizer
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes MRI_Fid_Localizer wait for user response (see UIRESUME)
% uiwait(handles.figure1);
set(handles.figure1,'WindowButtonDownFcn',@figure1_WindowButtonDownFcn)
set(handles.figure1,'pointer','cross')

% --- Outputs from this function are returned to the command line.
function varargout = MRI_Fid_Localizer_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in pmn_View.
function pmn_View_Callback(hObject, eventdata, handles)
% hObject    handle to pmn_View (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns pmn_View contents as cell array
%        contents{get(hObject,'Value')} returns selected item from pmn_View
handles.View=get(hObject,'value')
guidata(hObject,handles)

UpdateAxes(hObject,eventdata,handles)

% --- Executes during object creation, after setting all properties.
function pmn_View_CreateFcn(hObject, eventdata, handles)
% hObject    handle to pmn_View (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pb_OpenFile.
function pb_OpenFile_Callback(hObject, eventdata, handles)
% hObject    handle to pb_OpenFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%Select MR
[mrName]=spm_select(1,'image');
handles.data.mrName=mrName;

% get the mr into a structure
handles.data.mrStruct=spm_vol(handles.data.mrName);

% from structure to data matrix and xyz matrix (voxel coordinates)
[handles.data.mrData]=spm_read_vols(handles.data.mrStruct);
handles.data.mrData=handles.data.mrData/max(max(max(handles.data.mrData)));

% make data.elecMap for electrode positions
handles.data.elecMap=zeros(size(handles.data.mrData));

%Get View
handles.View=get(handles.pmn_View,'value');

guidata(hObject,handles)

UpdateAxes(hObject, eventdata, handles);

function UpdateAxes(hObject, eventdata, handles)

Z=round(get(handles.sl_Z,'Value'));
handles.View=get(handles.pmn_View,'value');

if isfield(handles.data,'elecMap') %if electrodes are there
    if handles.View==1
        rgbplaatje1=cat(3,0.5*handles.data.mrData(:,:,Z)+(handles.data.elecMap(:,:,Z)),...
            0.5*handles.data.mrData(:,:,Z),...
            0.5*handles.data.mrData(:,:,Z)+(handles.data.elecMap(:,:,Z)));
        imshow(rgbplaatje1,...
            'Parent',handles.axes1);
    elseif handles.View==2
        rgbplaatje2=cat(3,0.5*squeeze(handles.data.mrData(:,Z,:))+squeeze((handles.data.elecMap(:,Z,:))),...
            0.5*squeeze(handles.data.mrData(:,Z,:)),...
            0.5*squeeze(handles.data.mrData(:,Z,:))+squeeze((handles.data.elecMap(:,Z,:))));
        imshow(rgbplaatje2,...
            'Parent',handles.axes1);
    elseif handles.View==3     
        rgbplaatje3=cat(3,0.5*squeeze(handles.data.mrData(Z,:,:))+squeeze((handles.data.elecMap(Z,:,:))),...
            0.5*squeeze(handles.data.mrData(Z,:,:)),...
            0.5*squeeze(handles.data.mrData(Z,:,:))+squeeze((handles.data.elecMap(Z,:,:))));
        imshow(rgbplaatje3,...
            'Parent',handles.axes1);
    end
else
    if handles.View==1
        imshow(handles.data.mrData(:,:,Z),...
            'Parent',handles.axes1);
        hold on
    elseif handles.View==2
        imshow(squeeze(handles.data.mrData(:,Z,:)),...
            'Parent',handles.axes1);
        hold on
    elseif handles.View==3
        imshow(squeeze(handles.data.mrData(Z,:,:)),...
            'Parent',handles.axes1);
        hold on
    end
    colormap('gray');
end

guidata(hObject,handles)


% --- Executes on slider movement.
function sl_Z_Callback(hObject, eventdata, handles)
% hObject    handle to sl_Z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
UpdateAxes(hObject, eventdata, handles);

function sl_Z_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sl_Z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on mouse press over figure background.
function figure1_WindowButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles=guidata(hObject);

a=get(hObject,'CurrentPoint');
b=get(handles.axes1,'Position');
% c=get(handles.axes2,'Position');
% d=get(handles.axes3,'Position');
if handles.View==1
    if a(1)>b(1) && a(1)<b(1)+b(3) && a(2)>b(2) && a(2)<b(2)+b(4)

        xy=get(handles.axes1,'CurrentPoint'); %current point x and y

        %check for click within image
        if xy(1,2)>5 && xy(1,2)<=length(handles.data.mrData(:,1,1))-5 && ...
            xy(1,1)>5 && xy(1,1)<=length(handles.data.mrData(1,:,1))-5 % I do not know for sure whether X and Y are correct here
            % if already an electrode in that position remove
            if handles.data.elecMap(round(xy(1,2)),round(xy(1,1)),round(get(handles.sl_Z,'Value')))>0;
                removeElec(hObject, eventdata, handles,xy);
            else
                drawElec(hObject, eventdata, handles,xy);
            end
        end
    else
        %set(handles.display_feedback,'String','mis');
    end
elseif handles.View==2
    if a(1)>b(1) && a(1)<b(1)+b(3) && a(2)>b(2) && a(2)<b(2)+b(4)
       xy=get(handles.axes1,'CurrentPoint'); %current point x and y
        %check for click within image
        if xy(1,2)>5 && xy(1,2)<=length(handles.data.mrData(:,1,1))-5 && ...
            xy(1,1)>5 && xy(1,1)<=length(handles.data.mrData(1,1,:))-5 % I do not know for sure whether X and Y are correct here
            % if already an electrode in that position remove
            if handles.data.elecMap(round(xy(1,2)),round(get(handles.sl_Z,'Value')),round(xy(1,1)))>0;
                %drawElec(hObject, eventdata, handles,xy);
                removeElec(hObject, eventdata, handles,xy);
            else
                drawElec(hObject, eventdata, handles,xy);
            end
        end
    else
        %set(handles.display_feedback,'String','mis');
    end
elseif handles.View==3
    if a(1)>b(1) && a(1)<b(1)+b(3) && a(2)>b(2) && a(2)<b(2)+b(4)
       xy=get(handles.axes1,'CurrentPoint'); %current point x and y
        %check for click within image
        if xy(1,2)>5 && xy(1,2)<=length(handles.data.mrData(1,:,1))-5 && ...
            xy(1,1)>5 && xy(1,1)<=length(handles.data.mrData(1,1,:))-5 % I do not know for sure whether X and Y are correct here
            % if already an electrode in that position remove
            if handles.data.elecMap(round(get(handles.sl_Z,'Value')),round(xy(1,2)),round(xy(1,1)))>0;
                removeElec(hObject, eventdata, handles,xy);
            else
                drawElec(hObject, eventdata, handles,xy);
            end
        end
    else
        %set(handles.display_feedback,'String','mis');
    end
end


function drawElec(hObject, eventdata, handles,xy) 

% function that draws electrode

% set stuff
%radiusElect=str2double(get(handles.max_size,'String')); %5 in voxels, not mm
radiusElect=1;

    if handles.View==1
        current.XYZ=[round(xy(1,2)) round(xy(1,1)) round(get(handles.sl_Z,'Value'))];
    elseif handles.View==2
        current.XYZ=[round(xy(1,2)) round(get(handles.sl_Z,'Value')) round(xy(1,1))];
    elseif handles.View==3
        current.XYZ=[round(get(handles.sl_Z,'Value')) round(xy(1,2)) round(xy(1,1))];
    end
    

    % make an empty matrix for electrode locations
    data.elecMap=zeros(size(handles.data.mrData));
    % put ones on a box of radiusElect aournd where there was clicked
    data.elecMap(...
        current.XYZ(1)-radiusElect:current.XYZ(1)+radiusElect,...
        current.XYZ(2)-radiusElect:current.XYZ(2)+radiusElect,...
        current.XYZ(3)-radiusElect:current.XYZ(3)+radiusElect)=1;
    % put a 2 at the point were there was clicked
    data.elecMap(...
        current.XYZ(1),current.XYZ(2),current.XYZ(3))=2;
    
    % set data
    handles.data.elecMap(handles.data.elecMap==1|data.elecMap==1)=1;
    handles.data.elecMap(data.elecMap==2)=2;
%    set(handles.display_feedback,'String','found electrode');
    guidata(hObject,handles);
    UpdateAxes(hObject,eventdata,handles);
    
function removeElec(hObject, eventdata, handles,xy)
%set(handles.display_feedback,'String','removing electrode');
% function that removes electrode
if handles.View==1
current.XYZ=[round(xy(1,2)) round(xy(1,1)) round(get(handles.sl_Z,'Value'))];
elseif handles.View==2
current.XYZ=[round(xy(1,2)) round(get(handles.sl_Z,'Value')) round(xy(1,1))];
elseif handles.View==3
current.XYZ=[round(get(handles.sl_Z,'Value')) round(xy(1,2)) round(xy(1,1))];
end

data.elecMap=handles.data.elecMap;
data.elecMap(current.XYZ(1),current.XYZ(2),current.XYZ(3))=3;
data.elecMapV=data.elecMap(:);

%label blobs
data.elecMap_bwlabel=bwlabeln(data.elecMap);
data.elecMapV_bwlabel=data.elecMap_bwlabel(:);

% get label where the mouse clicked:
data.clickpointbool=(data.elecMapV==3);
data.clickpointbwlabel=data.elecMapV_bwlabel(data.clickpointbool);
data.correctlabelbool=(data.elecMapV_bwlabel==data.clickpointbwlabel);

% find blob with correct label
data.current_electV=data.correctlabelbool';
data.elecMapV(data.current_electV)=0;
data.elecMap(:)=data.elecMapV;

handles.data.elecMap=data.elecMap;
%set(handles.display_feedback,'String','removed electrode');
guidata(hObject,handles);
UpdateAxes(hObject,eventdata,handles);


% --- Executes on button press in pb_SaveEl.
function pb_SaveEl_Callback(hObject, eventdata, handles)
% hObject    handle to pb_SaveEl (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
elecMap=handles.data.elecMap;
dataOut=handles.data.mrStruct

% from structure to data matrix
data1.elec=spm_read_vols(dataOut);
[x,y,z]=ind2sub(size(data1.elec),find(elecMap>1.5));
% from indices 2 native
elecmatrix=([x y z]*dataOut.mat(1:3,1:3)')+repmat(dataOut.mat(1:3,4),1,length(x))';

[fn, pn, ~] = uiputfile( ...
       {'*.mat','MAT-files (*.mat)'}, ...
        'Save as', 'electrodes.mat');
    
save(fullfile(pn,fn),'elecmatrix')



% --- Executes on button press in pb_SaveFid.
function pb_SaveFid_Callback(hObject, eventdata, handles)
% hObject    handle to pb_SaveFid (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
elecMap=handles.data.elecMap;
dataOut=handles.data.mrStruct

% from structure to data matrix
data1.elec=spm_read_vols(dataOut);
[x,y,z]=ind2sub(size(data1.elec),find(elecMap>1.5));
% from indices 2 native
fiducial_locations=([x y z]*dataOut.mat(1:3,1:3)')+repmat(dataOut.mat(1:3,4),1,length(x))';

[fn, pn, ~] = uiputfile( ...
       {'*.mat','MAT-files (*.mat)'}, ...
        'Save as', 'MRI_Fiducials.mat');
    
save(fullfile(pn,fn),'fiducial_locations')


% --- Executes on button press in pb_VisualizeElectrodes.
function pb_VisualizeElectrodes_Callback(hObject, eventdata, handles)
% hObject    handle to pb_VisualizeElectrodes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
a=1;
