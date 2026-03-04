import maya.cmds as cmds

def validate_scene():
    issues = []

    # Check 1: Objects with history
    meshes = cmds.ls(type="mesh")
    for mesh in meshes:
        history = cmds.listHistory(mesh)
        if history and len(history) > 1:
            issues.append(f"{mesh} has construction history.")

    # Check 2: Unfrozen transforms
    transforms = cmds.ls(type="transform")
    for obj in transforms:
        if not cmds.objectType(obj, isType="joint"):
            t = cmds.getAttr(obj + ".translate")[0]
            r = cmds.getAttr(obj + ".rotate")[0]
            s = cmds.getAttr(obj + ".scale")[0]
            if t != (0.0, 0.0, 0.0) or r != (0.0, 0.0, 0.0) or s != (1.0, 1.0, 1.0):
                issues.append(f"{obj} has unfrozen transforms.")

    # Print issues
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("Scene is clean!")
        
validate_scene()

def create_ui():
    if cmds.window("sceneValidatorUI", exists=True):
        cmds.deleteUI("sceneValidatorUI")

    window = cmds.window("sceneValidatorUI", title="Scene Validator", widthHeight=(400, 300))
    cmds.columnLayout(adjustableColumn=True)

    cmds.button(label="Run Validation", command=lambda x: validate_scene())

    cmds.showWindow(window)

create_ui()