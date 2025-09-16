addDjangoApp() {
    local appName=$(readData "What is the app name?")

    local appFolder="api/$appName"
    mkdir -p "$appFolder"

    local adminFolder="$appFolder/admin"
    mkdir -p "$adminFolder"

    local migrationsFolder="$appFolder/migrations"
    mkdir -p "$migrationsFolder"

    local modelsFolder="$appFolder/models"
    mkdir -p "$modelsFolder"

    local serializersFolder="$appFolder/serializers"
    mkdir -p "$serializersFolder"

    local viewsFolder="$appFolder/views"
    mkdir -p "$viewsFolder"

    touch "$appFolder/__init__.py"
    
    local appsContext=$(getAppsContext $appName)
    echo "$appsContext" >> "$appFolder/apps.py"
    
    local urlsContext=$(getUrlsContext)
    echo "$urlsContext" >> "$appFolder/urls.py"

    echo "from django.contrib import admin" >> "$adminFolder/__init__.py"
    touch "$migrationsFolder/__init__.py"
    touch "$modelsFolder/__init__.py"
    touch "$serializersFolder/__init__.py"
    touch "$viewsFolder/__init__.py"

    echo -en "${I_YELLOW}"
    echo -e "Do not forget to add ${I_GREEN}$appName${I_YELLOW} to the list of INSTALLED_APPS in config.settings folder"
    echo -en "${DEFAULT_COLOR}"
    
}

createDjangoModel() {
    local appName=$(readData "To which Django app does this model belong?")
    local fileName=$(readData "What is the model file name (without .py)?")



    local appFolder="api/$appName"
    if [ ! -d "$appFolder" ]; then
        echo -e "${I_RED}The app '$appName' does not exist in your Django apps.\nIf you want to use this app, you first need to create it using addDjangoApp.${DEFAULT_COLOR}"
        return 1
    fi

    local modelsFolder="$appFolder/models"
    mkdir -p "$modelsFolder"

    local modelFileAddr="$modelsFolder/${fileName}.py"
    getDjangoModelContext >> "$modelFileAddr"

    echo "Done!"
    echo -en "${I_YELLOW}"
    echo -e "Please remember to import the models defined in ${fileName}.py into the __init__.py file in the models folder of the $appName app."
    echo -en "${DEFAULT_COLOR}"
    return 0
}

createDjangoSerializer() {
    local appName=$(readData "To which Django app does this serializer belong?")
    local fileName=$(readData "What is the serializer file name (without .py)?")



    local appFolder="api/$appName"
    if [ ! -d "$appFolder" ]; then
        echo -e "${I_RED}The app '$appName' does not exist in your Django apps.\nIf you want to use this app, you first need to create it using addDjangoApp.${DEFAULT_COLOR}"
        return 1
    fi

    local serializersFolder="$appFolder/serializers"
    mkdir -p "$serializersFolder"

    local serializerFileAddr="$serializersFolder/${fileName}.py"
    getDjangoSerializerContext >> "$serializerFileAddr"

    echo "Done!"
    echo -en "${I_YELLOW}"
    echo -e "Please remember to import the serializers defined in ${fileName}.py into the __init__.py file in the serializers folder of the $appName app."
    echo -en "${DEFAULT_COLOR}"
    return 0
}

createDjangoView() {
    local appName=$(readData "To which Django app does this view belong?")
    local fileName=$(readData "What is the view file name (without .py)?")



    local appFolder="api/$appName"
    if [ ! -d "$appFolder" ]; then
        echo -e "${I_RED}The app '$appName' does not exist in your Django apps.\nIf you want to use this app, you first need to create it using addDjangoApp.${DEFAULT_COLOR}"
        return 1
    fi

    local viewsFolder="$appFolder/views"
    mkdir -p "$viewsFolder"

    local viewFileAddr="$viewsFolder/${fileName}.py"
    getDjangoViewContext >> "$viewFileAddr"

    echo "Done!"
    echo -en "${I_YELLOW}"
    echo -e "Please remember to import the views defined in ${fileName}.py into the __init__.py file in the views folder of the $appName app."
    echo -e "Also, don't forget to add an endpoint URL for this viewset in the urls.py of the $appName app."
    echo -en "${DEFAULT_COLOR}"
    return 0
}

createDjangoAdminView() {
    local appName=$(readData "To which Django app does this admin file belong?")
    local fileName=$(readData "What is the admin file name (without .py)?")

    local appFolder="api/$appName"
    if [ ! -d "$appFolder" ]; then
        echo -e "${I_RED}The app '$appName' does not exist in your Django apps.\nIf you want to use this app, you first need to create it using addDjangoApp.${DEFAULT_COLOR}"
        return 1
    fi

    local adminFolder="$appFolder/admin"
    mkdir -p "$adminFolder"

    local adminFileAddr="$adminFolder/${fileName}.py"
    getDjangoAdminContext >> "$adminFileAddr"

    echo "Done!"
    echo -en "${I_YELLOW}"
    echo -e "Please remember to import the admin classes defined in ${fileName}.py into the __init__.py file in the admin folder of the $appName app.\nAlso, register your model with the admin site using: admin.site.register(YourModel, YourModelAdmin)."
    echo -en "${DEFAULT_COLOR}"
    return 0
}