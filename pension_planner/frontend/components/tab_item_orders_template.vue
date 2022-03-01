<template>
    <v-container>
        <v-row>
            <v-btn v-for="name in order_names" x-small @click=place_order(name)>
                <v-icon>mdi-plus-box</v-icon>
                {{name}}
            </v-btn>
        </v-row>
        <div v-for="w in control_widgets">
            <jupyter-widget :widget="w" />
        </div>
        <v-row>
            {{output}}

        </v-row>
    </v-container>
</template>