<script lang="ts">
    import type { Snippet } from "svelte";

    type IObjectChildItems = {
        title?: string;
        children: any;
    };

    const { title = "Associated Items", children }: IObjectChildItems = $props();
</script>

<div class="col-span-2 associated-card" id="children-info">
    <div class="associated-card-body">
        <h2 class="associated-card-title">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor">
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            {title}
        </h2>
        {@render children()}
    </div>
</div>
