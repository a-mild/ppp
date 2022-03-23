<template>
    <v-app-bar app>
        <v-app-bar-nav-icon
            id="toggle_sidebar_button"
            @click.stop="toggle_drawer()">
        </v-app-bar-nav-icon>
        <v-toolbar-title class=".text-h5">
                Pa's Pension Planner
                <div style="font-size: 0.6em">{{ loaded_filename }}</div>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <jupyter-widget :widget="upload_widget" />
        <v-btn
            icon
            @click="download_db()"
        >
            <v-icon>mdi-content-save</v-icon>
        </v-btn>
        <jupyter-widget :widget="download_output_dummy" />
    </v-app-bar>
</template>