<template>
<v-card>
    <v-card-title style="font-size: 1.0em">{{name}}</v-card-title>
    <v-card-actions>
      <v-btn
        text
        x-small
      >
        <v-icon>mdi-pencil</v-icon>
        Edit
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn
        @click="show_details = !show_details"
      >
          Details
        <v-icon>{{ show_details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
      </v-btn>
    </v-card-actions>
    <v-expand-transition>
      <div v-show="show_details">
        <v-divider></v-divider>

        <v-card-text>
          Details ...
        </v-card-text>
      </div>
    </v-expand-transition>
</v-card>
</template>