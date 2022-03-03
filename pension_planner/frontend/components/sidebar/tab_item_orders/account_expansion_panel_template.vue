<template>
</div>
<v-expansion-panel>
     <v-expansion-panel-header>{{name}}</v-expansion-panel-header>
     <v-expansion-panel-content>
         <v-container>
             <v-row>
                 <v-col>
                     <v-row>Einzahlungen</v-row>
                     <v-row v-for="asset in assets">
                         <jupyter-widget :widget="asset" />
                     </v-row>
                 </v-col>
                 <v-col >
                     <v-row>Auszahlungen</v-row>
                     <v-row v-for="liability in liabilities">
                         <jupyter-widget :widget="liabilitiy" />
                     </v-row>
                 </v-col>
             </v-row>
        </v-container>
    </v-expansion-panel-content>
</v-expansion-panel>
</div>
</template>