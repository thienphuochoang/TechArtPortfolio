--A function which is used to save defaults to a file
fn SaveToFile theTexLine =
(
	local ScriptsFolder = pathconfig.getdir #userscripts		
	local DefaultsFolder = pathconfig.appendPath ScriptsFolder "\\TexelDensityTool"
	local DefaultsFilePath = pathconfig.appendPath DefaultsFolder "\\defaults.ini"
			
	local WarningString = "--This is a default.ini file for Texel Density Tool\n--DO NOT EDIT THIS FILE MANUALLY\n\n"
	
	-- If file doesn't exist
	if not doesFileExist DefaultsFilePath then
	(
		--Create a directory
		makeDir DefaultsFolder			
		--Create a file
		local File = createFile DefaultsFilePath
		--OutPut to log
		format "% has been created\n" DefaultsFilePath
		
		--OutPut theTexLine to a file
		format "%%" WarningString theTexLine to: File 
		close File
		
		--OutPut to log
		format "Defaults for Texel Density Tool has been saved sucessfully in %\n" DefaultsFilePath
	)
	else
	(
		--Open an existing file for rewrite (deletes file contents if it exists)
		local File = openFile DefaultsFilePath mode:"w" 
		
		--OutPut theTexLine to a file
		format "%%" WarningString theTexLine to: File 
		close File
		
		--OutPut to log
		format "Defaults for Texel Density Tool has been saved sucessfully in %\n" DefaultsFilePath
	)
		
) --end of fuction

--Function that scales selected UVs by a Multiplier around specific Pivot in a selected Direction e.g.: UVScaleByPivot 2 "UV" "TopLeft"
fn UVScaleByPivot ScaleMultiplier ScaleDirection PivotMode =
(
	local uvw_mod = modpanel.getcurrentobject()
		
	local  pm = case PivotMode of
	(
			"Center":1
			"Top":7
			"Bottom":3
			"Left":9
			"Right":5
			
			"TopLeft":8
			"Top-Left":8
			"LeftTop":8
			"Left-Top":8
		
			"TopRight":6
			"Top-Right":6
			"RightTop":6
			"Right-Top":6	
		
			"BottomLeft":2
			"Bottom-Left":2
			"LeftBottom":2
			"Left-Bottom":2
		
			"BottomRight":4
			"Bottom-Right":4
			"RightBottom":4
			"Right-Bottom":4
			
	)		
	
	local sd = case ScaleDirection of
	(
		"U":point2 ScaleMultiplier 1 
		"V":point2 1 ScaleMultiplier
		"UV":point2 ScaleMultiplier ScaleMultiplier
	)
		
	--Offset pivot for the shape
	uvw_mod.snapPivot pm 
	--Calculate world UV position for pivot
	local PivotPosition = (uvw_mod.getPivotOffset() + uvw_mod.getSelCenter())
	
	--Scale UV Shells		
	uvw_mod.scaleSelectedXY sd.x sd.y PivotPosition
		
	
) --end of function

--Function that return value from a Position in sequence of values. e.g. in a line "<5> <7>" and Pos = 2 it will return 7
fn LoadValueFromFile ValuePosition =
(
	local ScriptsFolder = pathconfig.getdir #userscripts		
	local DefaultsFolder = pathconfig.appendPath ScriptsFolder "\\TexelDensityTool"
	local DefaultsFilePath = pathconfig.appendPath DefaultsFolder "\\defaults.ini"			
	
	local FilePosition
	local ReturnValue = ""
	
	-- If file exist
	if doesFileExist DefaultsFilePath then
	(
		--Local counter for iterations
		local I = 1
		--Open File for read-only
		local File = openFile DefaultsFilePath mode:"r" 
		
		--Search for "<" symbol
		if (skipToString File "<") == undefined do
		(	
			seek File 0 --Go to the beginning of the file			
			close File
			return undefined
		)		
		
		--while not end of file
		while (not eof File) do
		(									
			--Read character to memory
			local c = readChar File			
			
			--If Postion is found
			if ValuePosition == I then 
			(
				--While c is not ">" collect to ReturnValue and take a next character and then - exit
				While (not c == ">") and (not eof File) do	
				(
					ReturnValue += c 	
					c = readChar File
				)					
				exit			
			)			
			else --skip to next
			(
					--Next I
					I += 1
					--Skip to "<" symbol
					While (not c == "<") and (not eof File) do c = readChar File 
			)
		)					
	)
	else
	return undefined
	
	seek File 0 --Go to the beginning of the file			
	close File
	return ReturnValue
) --end of fuction

--Function to calculate how many "meters" in system units
fn GetMetersFromGU = 
(
	local meters = case units.systemType of
	(
		#Inches: 0.0254
		#Feet: 0.3048
		#Miles: 1609.0
		#Millimeters: 0.001
		#Centimeters: 0.01
		#Meters: 1.0
		#Kilometers: 1000.0
	)
	return meters*units.SystemScale --return value
) --end of fuction

--Let's create a function to acknowledge Texel Density
fn GetTexelDensity w h =
(
	--Check the Modifier Class whether it is unwrap_uvw or not
	if classof (unwrapmod = modpanel.getcurrentobject()) == unwrap_uvw do
	(
		--Make an array of selected Faces
		if (faces = unwrapmod.getselectedfaces()).count > 0 do
		(
			-- Get some information about the selection
			unwrapmod.getarea faces &mX &mY &mWidth &mHeight &mAreaUVW &mAreaGeom

			-- Calculate the total texture area
-- 			textureArea = theMapSize^2
			textureArea = w*h
			-- Calculate the used area
			usedAreaPixels = mAreaUVW * textureArea

			-- Calculate the texel density
			texelDensity = sqrt (usedAreaPixels/mAreaGeom)
			-- break()
		)
	)
	texelDensity --return value
) --end of fuction

--Try to destroy previous rollout
try(destroyDialog rol_UVTexelDensity)catch()

--Creating new Rollout
rollout rol_UVTexelDensity "Texel Density Tool" 
(
	--defining local variables
	local theTexDen
	local theTexDenCluster
	local theMapSize = 0.0	
	local theTextureMapArea,theGeomArea,theUsedAreaPixels,theDefinedRatio
	local obj_ResolutionsArray = #(" 8192", " 4096", " 2048", " 1024", " 512", " 256", " 128")
	local thePivotPosition = "Top"
	local chkbtnBasePos = [14,100]
	local UnwrapError = "Please select an object"
	local ScalePannelState = false
	local checkMapBackupMat = #()
	local checkMapBackupObj = #()
	local checkMapMaterial
	local checkerMapList = #("checker_map_256x256.png", "checker_map_512x512.png", "checker_map_1024x1024.png", "checker_map_2048x2048.png")
	local countChecker = 1
	local userIconDirectory = getDir #usericons
	
	fn GetResolution ResolutionString = 
	(
		local theResolution = case ResolutionString of
		(
			" 8192": 8192
			" 4096": 4096
			" 2048": 2048
			" 1024": 1024
			" 512": 512
			" 256": 256
			" 128": 128
		)
		return theResolution
	)
	
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	--Interface	
	--Map Dimension and Texel Density
	spinner spnTexDens range:[0,8192,512] Pos:[120,19] width:55 height:16 type:#integer scale: 128 tooltip: "Texel density"
	
	dropdownlist drpdnMapSizew items:obj_ResolutionsArray Pos:[85,43] width:60 selection: 4 Tooltip: "Target map resolution"
	dropdownlist drpdnMapSizeh items:obj_ResolutionsArray Pos:[160,43] width:60 selection: 4 Tooltip: "Target map resolution"
	checkbox doubleSize Pos:[225,43] width:30 height:20 Tooltip: "Double Texture Size" checked:true
	--spinner spnMapSize "Map Size:" range:[0,8192,1024] Pos:[75,70] width:150 height:16 type:#integer scale:128	tooltip: "Map Size"
	
	--Labels
	label lblTDText "Texel\nDensity\n(Px/m)" Pos:[15,17] width:50 height:50
	label lblMSwText "w: " Pos:[72,46] width:10 height:15 Tooltip: "Target map resolution"
	label lblMShText "h: " Pos:[150,46] width:10 height:15 Tooltip: "Target map resolution"
	--Buttons 
	button btn_getTexelDensity "Get" Pos:[70,14] width:45 height:25 tooltip: "Gets texel density from a selected UV-Shells \n(Unwrap UVW modifier should be applied)"
	button btn_setTexelDensity "Set" Pos:[180,14] width:45 height:25 tooltip: "Sets texel density to a selected UV-Shells \n(Unwrap UVW modifier should be applied)"
	
	--button btnCheckerMap "Checker Map" pos:[85,69] width:25 height:25 images:#(@"\\glassegg.com\TOOLS\TECHNICAL_SCRIPT\Projects\NetEase_Evn_19\Scripts\icon\checker_icon.jpg", undefined, 1, 1, 1, 1, 1)
	--spinner spn8 "" pos:[129,74] width:60 height:16 enabled:true range:[0,100,0]
	button btnTexelMaterial "" pos:[32,68] width:24 height:24 images:#(userIconDirectory + "\\" + "checker_material.jpg", undefined, 1, 1, 1, 1, 1)
	button chbCheckChecker "Button" pos:[72,68] width:24 height:24 images:#(userIconDirectory + "\\" + "checker_icon.jpg", undefined, 1, 1, 1, 1, 1)
	button btnReset "Reset" pos:[212,68] width:24 height:24 images:#(userIconDirectory + "\\" + "reset.jpg", undefined, 1, 1, 1, 1, 1)
	spinner spn_TilingUV1 "U" pos:[102,72] width:41 height:20 align:#left range:[0,100,1]
	spinner spn_TilingUV2 "V" pos:[152,72] width:41 height:20 align:#left range:[0,100,1]
	--spinner spnValueChecker Pos:[107,72] range:[0,100,1.0] width:60 height:25 type:#float scale: 0.1 tooltip: "Checker Map Ratio"
	
	button btn_Separator_Down "v" tooltip:"Open Scale By Value Section" Pos: [0, 98] width:240 height:10 border:true
	button btn_Separator_UP "^" tooltip:"Close Scale By Value Section" Pos: [0, 178] width:240 height:10 border:true
	
	--Scale By Value
	label lbl_Scale "Scale by Value:" Pos: [72, 110] tooltip: "Scales Selected UV-Shells by a value \n(Unwrap UVW modifier should be applied)"
	spinner spn_Scale Pos:[72,130] range:[0,100,2] width:60 height:25 type:#float scale: 0.01 tooltip: "Scale Factor"
	
	checkbutton chkbtn_U "U" checked:true tooltip:"Scale Horizontally" Pos: [135,130] width:18 height:16
	checkbutton chkbtn_V "V" checked:true tooltip:"Scale Vertically" Pos: [155,130] width:18 height:16
	
	button btn_Scale "Scale by Value" Pos:[72,150] width:101 height:25 tooltip: "Scales Selected UV-Shells by a value \n(Unwrap UVW modifier should be applied)"


	button btn_Half "x0.5" Pos:[180,125] width:45 height:25 tooltip: "Scales selected UV-Shells by half \n(Unwrap UVW modifier should be applied)"
	button btn_Double "x2" Pos:[180,150] width:45 height:25 tooltip: "Doubles the scale of selected UV-Shells \n(Unwrap UVW modifier should be applied)"
	
	
	
	
	--Pivot Section
	label lblPivot "Pivot:" Pos: [chkbtnBasePos.x+3, chkbtnBasePos.y+10] tooltip: "Sets pivot for scaling of selected UV-Shells"
			
	checkbutton chkbtnTopLeft "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Top Left Corner" Pos: [chkbtnBasePos.x,chkbtnBasePos.y+30] width:12 height:12
	checkbutton chkbtnTop "" checked:true tooltip:"Sets pivot for scaling of selected UV-Shells to Selection Top" Pos: [chkbtnBasePos.x+17,chkbtnBasePos.y+30] width:12  height:12 
	checkbutton chkbtnTopRight "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Top Right Corner" Pos: [chkbtnBasePos.x+34,chkbtnBasePos.y+30] width:12 height:12
	
	checkbutton chkbtnLeft "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Selection Left" Pos:[chkbtnBasePos.x,chkbtnBasePos.y+47] width:12 height:12
	checkbutton chkbtnCenter "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Selection Center" Pos:[chkbtnBasePos.x+17,chkbtnBasePos.y+47] width:12 height:12
	checkbutton chkbtnRight "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Selection Right" Pos:[chkbtnBasePos.x+34,chkbtnBasePos.y+47]width:12 height:12
	
	checkbutton chkbtnBottomLeft "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Bottom Left Corner" Pos:[chkbtnBasePos.x,chkbtnBasePos.y+62] width:12 height:12
	checkbutton chkbtnBottom "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Selection Bottom" Pos:[chkbtnBasePos.x+17,chkbtnBasePos.y+62] width:12 height:12
	checkbutton chkbtnBottomRight "" checked:false tooltip:"Sets pivot for scaling of selected UV-Shells to Bottom Right Corner" Pos:[chkbtnBasePos.x+34,chkbtnBasePos.y+62] width:12 height:12
	
	----------------------------------------------------------------------------------------------------------------------------------------------------------
	
	--Update variables when values changes
	on spnTexDens changed val do theTexDen = val * (GetMetersFromGU())
	--on spnMapSize changed val do theMapSize = val	
		
	--function that unpress all the checkbuttons
	fn UnpressButtons = 
	(
			chkbtnTop.checked = false
			chkbtnTopRight.checked = false
			chkbtnTopLeft.checked = false
			
			chkbtnLeft.checked = false
			chkbtnCenter.checked = false
			chkbtnRight.checked = false
			
			chkbtnBottomLeft.checked = false
			chkbtnBottom.checked = false
			chkbtnBottomRight.checked = false
	)	--end of function
	
	--Function that presseses a corresponding check button
	fn PressCorrespondingBtn thePivotPosition =
	(
		UnpressButtons()
		case thePivotPosition of
		(
			
			"Center": chkbtnCenter.checked = true
			"Top": chkbtnTop.checked = true
			"Bottom": chkbtnBottom.checked = true
			"Left": chkbtnLeft.checked = true
			"Right": chkbtnRight.checked = true
			
			"TopLeft": chkbtnTopLeft.checked = true
			"Top-Left": chkbtnTopLeft.checked = true
			"LeftTop": chkbtnTopLeft.checked = true
			"Left-Top": chkbtnTopLeft.checked = true
		
			"TopRight": chkbtnTopRight.checked = true
			"Top-Right": chkbtnTopRight.checked = true
			"RightTop": chkbtnTopRight.checked = true
			"Right-Top": chkbtnTopRight.checked = true	
		
			"BottomLeft": chkbtnBottomLeft.checked = true
			"Bottom-Left": chkbtnBottomLeft.checked = true
			"LeftBottom": chkbtnBottomLeft.checked = true
			"Left-Bottom": chkbtnBottomLeft.checked = true
		
			"BottomRight": chkbtnBottomRight.checked = true
			"Bottom-Right": chkbtnBottomRight.checked = true
			"RightBottom": chkbtnBottomRight.checked = true
			"Right-Bottom": chkbtnBottomRight.checked = true
		)
	) --end of function
	
	--On Pivot selected
	on chkbtnTopLeft changed theState do
	(			
		thePivotPosition = "Top-Left"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnTop changed theState do
	(			
		thePivotPosition = "Top"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnTopRight changed theState do
	(
		thePivotPosition = "Top-Right"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnLeft changed theState do
	(
		thePivotPosition = "Left"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnCenter changed theState do
	(
		thePivotPosition = "Center"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnRight changed theState do
	(
		thePivotPosition = "Right"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnBottomLeft changed theState do
	(
		thePivotPosition = "Bottom-Left"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnBottom changed theState do
	(
		thePivotPosition = "Bottom"
		PressCorrespondingBtn (thePivotPosition)
	)
	
	on chkbtnBottomRight changed theState do
	(
		thePivotPosition = "Bottom-Right"
		PressCorrespondingBtn (thePivotPosition)
	)
	on chbCheckChecker pressed do
	(
		if selection != undefined do
		(
			checkerMat = Standardmaterial()
			checkerMat.name = "Puzzle_Checker_Material"
			tempArray = filterString userIconDirectory "\\"
			checkerPath = ""
			for i=1 to tempArray.count do
			(
				if i == tempArray.count then
				(
					break
				)
				else
				(
					checkerPath = checkerPath + tempArray[i] + "\\"
				)
			)
			checkerPath = checkerPath + "resource" + "\\" + "checkers"
			for i in selection do
			(
				if i.material != undefined then
				(
					if i.material.name != "Puzzle_Checker_Material" do
					(
						append checkMapBackupMat i.material
						append checkMapBackupObj i
					)
					if checkerMapList[countChecker] != undefined then
					(
						checkerFullPath = checkerPath + "\\" + checkerMapList[countChecker]
						checkerMat.diffuseMap = Bitmaptexture filename:checkerFullPath
						checkerMat.diffuseMap.coords.U_Tiling = spn_TilingUV1.value
						checkerMat.diffuseMap.coords.V_Tiling = spn_TilingUV2.value
						chbCheckChecker.images = #(checkerFullPath, undefined, 1, 1, 1, 1, 1)
						countChecker = countChecker + 1
						i.material = checkerMat
					)
					else
					(
						countChecker = 1
						checkerFullPath = CheckerPath + "\\" + checkerMapList[countChecker]
						checkerMat.DiffuseMap = Bitmaptexture filename:checkerFullPath
						checkerMat.diffuseMap.coords.U_Tiling = spn_TilingUV1.value
						checkerMat.diffuseMap.coords.V_Tiling = spn_TilingUV2.value
						chbCheckChecker.images = #(checkerFullPath, undefined, 1, 1, 1, 1, 1)
						countChecker = countChecker + 1
						i.material = checkerMat
					)
				)
				else
				(
					tempMat = Standardmaterial()
					i.material = tempMat
					if i.material.name != "Puzzle_Checker_Material" do
					(
						append checkMapBackupMat i.material
						append checkMapBackupObj i
					)
					if checkerMapList[countChecker] != undefined then
					(
						checkerFullPath = checkerPath + "\\" + checkerMapList[countChecker]
						checkerMat.diffuseMap = Bitmaptexture filename:checkerFullPath
						checkerMat.diffuseMap.coords.U_Tiling = spn_TilingUV1.value
						checkerMat.diffuseMap.coords.V_Tiling = spn_TilingUV2.value
						chbCheckChecker.images = #(checkerFullPath, undefined, 1, 1, 1, 1, 1)
						countChecker = countChecker + 1
						i.material = checkerMat
					)
					else
					(
						countChecker = 1
						checkerFullPath = CheckerPath + "\\" + checkerMapList[countChecker]
						checkerMat.DiffuseMap = Bitmaptexture filename:checkerFullPath
						checkerMat.diffuseMap.coords.U_Tiling = spn_TilingUV1.value
						checkerMat.diffuseMap.coords.V_Tiling = spn_TilingUV2.value
						chbCheckChecker.images = #(checkerFullPath, undefined, 1, 1, 1, 1, 1)
						countChecker = countChecker + 1
						i.material = checkerMat
					)
				)
			)
		)
	)
	on btnReset pressed do
	(
		print checkMapBackupObj
		for i=1 to checkMapBackupObj.count do
		(
			try
			(
				checkMapBackupObj[i].material = checkMapBackupMat[i]
			)
			catch()
		)
	)
	on spn_TilingUV1 changed value do
	(
		if selection != undefined do
		(
			for obj in selection do
			(
				if obj.mat.name == "Puzzle_Checker_Material" do
				(
					obj.mat.diffuseMap.coords.U_Tiling = value
				)
			)
		)
	)
	on spn_TilingUV2 changed value do
	(
		if selection != undefined do
		(
			for obj in selection do
			(
				if obj.mat.name == "Puzzle_Checker_Material" do
				(
					obj.mat.diffuseMap.coords.V_Tiling = value
				)
			)
		)
	)

	on btnTexelMaterial pressed do
	(
		break
	)
	--End of On Pivot selected

	----------------------------------------------------------------------------------------------------------------------------------
	
	------------------------------------------- ON ROL_UVTEXELDENSITY OPEN --------------------------------------------
	
	----------------------------------------------------------------------------------------------------------------------------------
	
	--Initialize variables on start
	on rol_UVTexelDensity open do
	(
		if (LoadValueFromFile 0) != undefined do			
		(
			try
			(
				spnTexDens.value = (LoadValueFromFile 1) as integer
				drpdnMapSize.selection = (LoadValueFromFile 2) as integer
				spn_Scale.value = (LoadValueFromFile 5) as float
				chkbtn_U.checked = (LoadValueFromFile 6) as booleanClass
				chkbtn_V.checked = (LoadValueFromFile 7) as booleanClass
				thePivotPosition = (LoadValueFromFile 8)
				PressCorrespondingBtn (thePivotPosition)
			)
			catch ()
			)				
	) --End initialize

	--button Scale By Value
	on btn_Scale pressed do
	(
		if selection.count > 0 do
		(
			if classof (modpanel.getcurrentobject()) != Unwrap_UVW do
			(
				setCommandPanelTaskMode mode:#modify
				addmodifier selection[1] (unwrap_UVW())
			)
		)
		if modpanel.getcurrentobject() != undefined and classof (modpanel.getcurrentobject()) == Unwrap_UVW then
		(		
			if chkbtn_U.checked and not chkbtn_V.checked then
			(
				UVScaleByPivot spn_Scale.value "U" thePivotPosition
			)
			else if not chkbtn_U.checked and chkbtn_V.checked then
			(
				UVScaleByPivot spn_Scale.value "V" thePivotPosition
			)
			else if chkbtn_U.checked and chkbtn_V.checked do
			(
				UVScaleByPivot spn_Scale.value "UV" thePivotPosition	
			)		
		)
		else messagebox UnwrapError		
	)
	--end of button Scale By Value
	
	--button Half
	on btn_Half pressed do
	(
		if selection.count > 0 do
		(
			if classof (modpanel.getcurrentobject()) != Unwrap_UVW do
			(
				setCommandPanelTaskMode mode:#modify
				addmodifier selection[1] (unwrap_UVW())
			)
		)
		if modpanel.getcurrentobject() != undefined and classof (modpanel.getcurrentobject()) == Unwrap_UVW then
		(
			if chkbtn_U.checked and not chkbtn_V.checked then
			(
				UVScaleByPivot 0.5 "U" thePivotPosition
			)
			else if not chkbtn_U.checked and chkbtn_V.checked then
			(
				UVScaleByPivot 0.5 "V" thePivotPosition
			)
			else if chkbtn_U.checked and chkbtn_V.checked do
			(
				UVScaleByPivot 0.5 "UV" thePivotPosition	
			)		
		)
		else messagebox UnwrapError		
	)
	--end of button Scale By Value
	
	--button Double
	on btn_Double pressed do
	(
		if selection.count > 0 do
		(
			if classof (modpanel.getcurrentobject()) != Unwrap_UVW do
			(
				setCommandPanelTaskMode mode:#modify
				addmodifier selection[1] (unwrap_UVW())
			)
		)
		if modpanel.getcurrentobject() != undefined and classof (modpanel.getcurrentobject()) == Unwrap_UVW then
		(
			if chkbtn_U.checked and not chkbtn_V.checked then
			(
				UVScaleByPivot 2 "U" thePivotPosition
			)
			else if not chkbtn_U.checked and chkbtn_V.checked then
			(
				UVScaleByPivot 2 "V" thePivotPosition
			)
			else if chkbtn_U.checked and chkbtn_V.checked do
			(
				UVScaleByPivot 2 "UV" thePivotPosition	
			)		
		)
		else messagebox UnwrapError		
	)
	--end of button Scale By Value
	
	--button get texel density
	on btn_getTexelDensity pressed do
	(
		theMapSizew = (GetResolution (drpdnMapSizew.selected))	
		theMapSizeh = (GetResolution (drpdnMapSizeh.selected))	
		if selection.count > 0 do
		(
			if classof (modpanel.getcurrentobject()) != Unwrap_UVW do
			(
				setCommandPanelTaskMode mode:#modify
				addmodifier selection[1] (unwrap_UVW())
			)
		)
		if modpanel.getcurrentobject() != undefined and classof (modpanel.getcurrentobject()) == Unwrap_UVW then
		(
			spnTexDens.value =  (GetTexelDensity theMapSizew theMapSizeh)/(GetMetersFromGU())				
			theTexDen = spnTexDens.value * (GetMetersFromGU())
		)
		else messagebox UnwrapError		
	)
	--end of get texel density script


	--button Set
	on btn_setTexelDensity pressed do
	(
		theTexDen = spnTexDens.value * (GetMetersFromGU())	
		theMapSizew = (GetResolution (drpdnMapSizew.selected))	
		theMapSizeh = (GetResolution (drpdnMapSizeh.selected))	
		undo "Set Texel Density" on
		(				
			if theTexDen >0 then
			(
				if selection.count > 0 do
				(
					if classof (modpanel.getcurrentobject()) != Unwrap_UVW do
					(
						setCommandPanelTaskMode mode:#modify
						addmodifier selection[1] (unwrap_UVW())
					)
				)
				if modpanel.getcurrentobject() != undefined and classof (modpanel.getcurrentobject()) == Unwrap_UVW then
				(
					----it will rescale the cluster to equalize the texel density
					actionMan.executeAction 2077580866 "40207"

					-- In this short script 'c' is defining the cluster
					texelDensityCluster = GetTexelDensity theMapSizew theMapSizeh
					format "Texel Density Cluster: %\n" texelDensityCluster

					--it will acknowledge the texel density of cluster so we can define the ratio
					--getting the ratio between single face and cluster
					theDefinedRatio=(theTexDen/texelDensityCluster)
					theUnwrapmod = modpanel.getcurrentobject()
					theUnwrapmod.scaleSelectedCenter theDefinedRatio 0
				) else messagebox UnwrapError
			)
				else messagebox "Please set Texel Density correctly."
			--end of Normalization
		)
	)
		----end of button Set

	on btn_Separator_Down pressed do
	(		
		
		if ScalePannelState == false then rol_UVTexelDensity.height = 190
		else rol_UVTexelDensity.height = 110
		
		ScalePannelState = not ScalePannelState			
		btn_Separator_Down.visible = not btn_Separator_Down.visible			
	)
	
	on btn_Separator_UP pressed do
	(		
		
		if ScalePannelState == false then rol_UVTexelDensity.height = 190
		else rol_UVTexelDensity.height = 110
		
		ScalePannelState = not ScalePannelState			
		btn_Separator_Down.visible = not btn_Separator_Down.visible			
	)
	
	on drpdnMapSizew selected e do (
		if doubleSize.checked == true then (
			drpdnMapSizeh.selection = drpdnMapSizew.selection
		)
	)
	
	on drpdnMapSizeh selected e do (
		if doubleSize.checked == true then (
			drpdnMapSizew.selection = drpdnMapSizeh.selection
		)
	)
	
	on doubleSize changed e do (
		if doubleSize.checked == true then (
			drpdnMapSizeh.selection = drpdnMapSizew.selection
		)
	)		
	
	on rol_UVTexelDensity close do 
	(
		local theDialogPos = GetDialogPos rol_UVTexelDensity
		
		theTextToSave = "<" + spnTexDens.value as string + "><" + drpdnMapSizew.selection as string + "><" +  theDialogPos.x as string + "><" + theDialogPos.y as string + "><" + spn_Scale.value as string + ">"
		theTextToSave += "<" + chkbtn_U.checked as string + "><" + chkbtn_V.checked as string + ">"
		theTextToSave += "<" + thePivotPosition + ">"
		SaveToFile theTextToSave
	)
	
	--on chbCheckChecker pressed do
	--(
		--include "//glassegg.com/TOOLS/TECHNICAL_SCRIPT/Projects/Environment_Default/Max/checker/app/bin/rEnvironment_Default_CheckerMat.ms"
	--)
	/*
	on spnValueChecker changed value do
	(
		try
		(
			if checkMapBackupObj.count != 0 do
			(
				if checkMapMaterial.diffuseMap != undefined do
				(
					checkMapMaterial.diffuseMap.coords.realWorldHeight = value
					checkMapMaterial.diffuseMap.coords.realWorldWidth = value
				)
			)
		)
		catch()
	)
	*/
	
)
--end of full script


if (LoadValueFromFile 0) != undefined then	
(
	createDialog rol_UVTexelDensity width:240 height:110 Pos: [(LoadValueFromFile 3) as integer, (LoadValueFromFile 4) as integer]  style:#(#style_toolwindow, #style_sysmenu) 			
)
else	createDialog rol_UVTexelDensity width:240 height:110 Pos:[1300,230]  style:#(#style_toolwindow, #style_sysmenu) 	

--end of rollout