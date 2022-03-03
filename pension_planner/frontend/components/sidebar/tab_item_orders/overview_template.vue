<div>
<v-expansion-panels accordion>
    <jupyter-widget v-for="acc in accounts" :widget="acc" />
    {{output}}
</v-expansion-panels>
</div>
