%%
% Compares uniques between annotators

%% Drawing
figure
hold all
plot3(c(:,3),c(:,4),c(:,5),'.')
plot3(c(1,3),c(1,4),c(1,5),'.','MarkerSize',50)

%% Create pairs
ind          = find(c(:,7)==-1);
c(ind,7)     = c(ind,1);
cstarts      = c(:,3:5); 
cends        = c(c(:,7),3:5);
plot3([cstarts(:,1) cends(:,1)]',[cstarts(:,2) cends(:,2)]',[cstarts(:,3) cends(:,3)]','r') %consensus

ind         = find(b(:,7)==-1);
b(ind,7)    = b(ind,1);
bstarts     = b(:,3:5); 
bends       = b(b(:,7),3:5);
%plot3([bstarts(:,1) bends(:,1)]',[bstarts(:,2) bends(:,2)]',[bstarts(:,3) bends(:,3)]','b') %base

ind         = find(u1(:,7)==-1);
u1(ind,7)    = u1(ind,1);
u1starts     = u1(:,3:5); 
u1ends       = u1(u1(:,7),3:5);
%plot3([u1starts(:,1) u1ends(:,1)]',[u1starts(:,2) u1ends(:,2)]',[u1starts(:,3) u1ends(:,3)]','g') %unique 1

ind         = find(u2(:,7)==-1);
u2(ind,7)    = u2(ind,1);
u2starts     = u2(:,3:5); 
u2ends       = u2(u2(:,7),3:5);
%plot3([u2starts(:,1) u2ends(:,1)]',[u2starts(:,2) u2ends(:,2)]',[u2starts(:,3) u2ends(:,3)]','y') %unique 2

%%  Length
Lc          = sum(sqrt(sum((cends-cstarts).^2,2)))
Lb          = sum(sqrt(sum((bends-bstarts).^2,2)))
Lu1         = sum(sqrt(sum((u1ends-u2starts).^2,2)))
Lu2         = sum(sqrt(sum((u2ends-u2starts).^2,2)))

%% Calculations
Ldif        = Lc-Lb
Lratio      = Lb/Lc

fpositives   = ((Lu1+Lu2)-(Ldif))/(Lu1+Lu2)
tpositives   = 1-fpositives
