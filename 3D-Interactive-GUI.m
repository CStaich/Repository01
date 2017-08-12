function varargout = Noodles(varargin)
% NOODLES MATLAB code for Noodles.fig
%      NOODLES, by itself, creates a new NOODLES or raises the existing
%      singleton*.
%
%      H = NOODLES returns the handle to a new NOODLES or the handle to
%      the existing singleton*.
%
%      NOODLES('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in NOODLES.M with the given input arguments.
%
%      NOODLES('Property','Value',...) creates a new NOODLES or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Noodles_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Noodles_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Noodles

% Last Modified by GUIDE v2.5 13-Apr-2017 17:24:06

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Noodles_OpeningFcn, ...
                   'gui_OutputFcn',  @Noodles_OutputFcn, ...
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


% --- Executes just before Noodles is made visible.
function Noodles_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Noodles (see VARARGIN)

% Choose default command line output for Noodles
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Noodles wait for user response (see UIRESUME)
% uiwait(handles.figure1);
r = 1;
armDensity = 8;
bump_depth = .25;
asize = 2;

theta = linspace(0,2*pi,300);
phi = linspace(-pi/2,pi/2,300);
[theta, phi] = meshgrid(theta,phi);
%rho = 1+.5*sin(theta*armDensity*2) + .5*cos((2*phi+pi)*armDensity);
theta_adj = theta./(2*pi);
phi_adj = (phi+pi/2)*2/(2*pi);
rho = (1-bump_depth) + bump_depth/2*cos((theta_adj*pi+pi)*armDensity) + bump_depth/2*cos((phi_adj*pi+pi)*armDensity);

[x, y, z] = sph2cart(theta, phi, rho);
surf(x,y,z,abs(rho));
h = rotate3d;
h.Enable = 'on';
h.RotateStyle = 'orbit';
shading interp;
colormap hsv;
daspect([1 1 1]);
axis off;
view(90,35);

% --- Outputs from this function are returned to the command line.
function varargout = Noodles_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in colorScheme.
function colorScheme_Callback(hObject, eventdata, handles)
% hObject    handle to colorScheme (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
colorScheme = get(handles.colorScheme,'Value');
switch colorScheme
    case 1
        colormap parula;
    case 2
        colormap jet;
    case 3
        colormap hsv;
    case 4
        colormap hot;
    case 5
        colormap cool;
    case 6
        colormap spring;
    case 7
        colormap summer;
    case 8
        colormap autumn;
    case 9
        colormap winter;
    case 10
        colormap gray;
    case 11
        colormap bone;
    case 12
        colormap copper;
    case 13
        colormap pink;
    case 14
        colormap lines;
    case 15
        colormap colorcube;
    case 16
        colormap prism;
    case 17
        colormap flag;
    case 18
        colormap white;
end;
% --- Executes during object creation, after setting all properties.
function colorScheme_CreateFcn(hObject, eventdata, handles)
% hObject    handle to colorScheme (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on slider movement.
function armDensity_Callback(hObject, eventdata, handles)
% hObject    handle to armDensity (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[az,el] = view;
armDensity = get(handles.armDensity,'Value');
armDensity = 2*floor(armDensity^(1.5))-20;
set(handles.armDensityDisplay,'String',armDensity);
bump_depth = get(handles.armDepth,'Value');
%regraph
theta = linspace(0,2*pi,300);
phi = linspace(-pi/2,pi/2,300);
[theta, phi] = meshgrid(theta,phi);
theta_adj = theta./(2*pi);
phi_adj = (phi+pi/2)*2/(2*pi);
rho = (1-bump_depth) + bump_depth/2*cos((theta_adj*pi+pi)*armDensity) + bump_depth/2*cos((phi_adj*pi+pi)*armDensity);
[x, y, z] = sph2cart(theta, phi, rho);
axes(handles.axes1);
surf(x,y,z,abs(rho));
%axis properties
h = rotate3d;
h.Enable = 'on';
h.RotateStyle = 'orbit';
shading interp;
daspect([1 1 1]);
axis off;
view([az,el]);

% --- Executes during object creation, after setting all properties.
function armDensity_CreateFcn(hObject, eventdata, handles)
% hObject    handle to armDensity (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function armDepth_Callback(hObject, eventdata, handles)
% hObject    handle to armDepth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
bump_depth = get(handles.armDepth,'Value');
[az,el] = view;
armDensity = get(handles.armDensity,'Value');
armDensity = 2*floor(armDensity^(1.5))-20;
set(handles.armDensityDisplay,'String',armDensity);
set(handles.armDepthDisplay,'String',bump_depth*100);
%regraph
theta = linspace(0,2*pi,300);
phi = linspace(-pi/2,pi/2,300);
[theta, phi] = meshgrid(theta,phi);
%rho = 1+.5*sin(theta*armDensity*2) + .5*cos((2*phi+pi)*armDensity);
theta_adj = theta./(2*pi);
phi_adj = (phi+pi/2)*2/(2*pi);
rho = (1-bump_depth) + bump_depth/2*cos((theta_adj*pi+pi)*armDensity) + bump_depth/2*cos((phi_adj*pi+pi)*armDensity);

[x, y, z] = sph2cart(theta, phi, rho);
surf(x,y,z,abs(rho));
h = rotate3d;
h.Enable = 'on';
h.RotateStyle = 'orbit';
shading interp;
daspect([1 1 1]);
axis off;

view([az,el]);

% --- Executes during object creation, after setting all properties.
function armDepth_CreateFcn(hObject, eventdata, handles)
% hObject    handle to armDepth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
