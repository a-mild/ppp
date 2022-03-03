<template>
    <div>
    <v-container>
        <v-row>
            <jupyter-widget :widget="place_order" />
        </v-row>
        <v-row>
            <jupyter-widget :widget="order_editor" />
        </v-row>
        <v-row>
            <jupyter-widget :widget="overview" />
        </v-row>
    </v-container>
    <v-expansion-panels accordion>
        <v-expansion-panel>
            <v-expansion-panel-header>Hallo welt</v-expansion-panel-header>
        </v-expansion-panel>
    </v-expansion-panels>
    </div>
</template>