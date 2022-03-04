<v-container>
    <v-row>
        <jupyter-widget :widget="name" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="from_acc_id" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="target_acc_id" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="date" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="start_date" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="end_date" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="amount" />
    </v-row>
    {{output}}
</v-container>