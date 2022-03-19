<v-container>
    <v-row>
        <jupyter-widget :widget="name" id="name"/>
    </v-row>
    <v-row>
        <jupyter-widget :widget="from_acc_id" id="from_acc_id"/>
    </v-row>
    <v-row>
        <jupyter-widget :widget="target_acc_id" id="target_acc_id"/>
    </v-row>
    <v-row>
        <jupyter-widget :widget="date" id="date" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="start_date" id="start_date" />
    </v-row>
    <v-row>
        <jupyter-widget :widget="end_date" id="end_date"/>
    </v-row>
    <v-row>
        <jupyter-widget :widget="amount" id="amount"/>
    </v-row>
    {{output}}
</v-container>