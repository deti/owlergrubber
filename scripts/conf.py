def read():
    import os
    import metayaml
    from attrdict import AttrDict

    def root_directory(application_path=None):
        root_path = application_path or os.path.dirname(__file__)
        while root_path and "bin" not in os.listdir(root_path):
            root_path = os.path.dirname(root_path)
        return root_path

    def config_directory():
        root_path = root_directory()
        return os.path.join(root_path, "configs", "stage")

    def fix_me():
        print("fix me")
        raise Exception("Required field is empty")

    stage_config = os.environ.get("OG_CONFIG", os.path.join(config_directory(), "dev.yaml"))

    configs = [os.path.join(root_directory(), "scripts", "configs", "og.yaml"),
               stage_config]
    config = metayaml.read(configs,
                           defaults={
                               "__FIX_ME__": fix_me,
                               "STAGE_DIRECTORY": config_directory(),
                               "join": os.path.join,
                               "ROOT": root_directory()
                           })
    config = AttrDict(config, recursive=True)
    for k in config.keys():
        if k == "__FIX_ME__":
            continue
        v = getattr(config, k)
        globals()[k] = v

    return config

read()

del globals()['read']