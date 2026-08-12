<script lang="ts">
    import type { RsvpQuestionSchema } from "$api-client";
    import { enhance } from "$app/forms";

    const { data } = $props();

    const rsvpQuestions: RsvpQuestionSchema[] = data.rsvpQuestions || [];
    const yesNoQuestions = $derived(rsvpQuestions.filter((question) => question.questionType === "yes_no"));
    const multipleChoiceQuestions = $derived(
        rsvpQuestions.filter((question) => question.questionType === "multiple_choice"),
    );
    const textQuestions = $derived(rsvpQuestions.filter((question) => question.questionType === "text"));

    let editingQuestionId = $state<string | null>(null);
    let editingChoiceId = $state<string | null>(null);
</script>

<div class="config-card">
    <div class="config-card-body">
        <h2 class="config-card-title text-xl mb-4">RSVP Questions</h2>
        <p>Manage Yes/No, Multiple Choice, and Text questions for RSVP accept flow.</p>

        <div class="divider divider-accent">Yes/No</div>
        <div class="grid grid-cols-1 gap-4 mt-4">
            {#each yesNoQuestions as question (question.id)}
                <div class="card bg-base-100 border border-base-300">
                    <div class="card-body p-4 gap-2">
                        {#if editingQuestionId === question.id}
                            <form
                                method="POST"
                                action="?/updateQuestion"
                                use:enhance={() => {
                                    return () => {
                                        editingQuestionId = null;
                                    };
                                }}>
                                <input type="hidden" name="questionId" value={question.id} />
                                <div class="flex flex-col gap-2">
                                    <label class="edit-card-field-name" for="text_{question.id}">Question Text</label>
                                    <input
                                        id="text_{question.id}"
                                        class="edit-card-field-input w-full"
                                        type="text"
                                        name="text"
                                        value={question.text}
                                        required />
                                    <label class="edit-card-field-name" for="order_{question.id}">Order</label>
                                    <input
                                        id="order_{question.id}"
                                        class="edit-card-field-input w-24"
                                        type="number"
                                        name="order"
                                        value={question.order}
                                        min="0" />
                                    <label class="edit-card-field-name" for="published_{question.id}">Status</label>
                                    <select
                                        id="published_{question.id}"
                                        class="edit-card-field-input w-40"
                                        name="published">
                                        <option value="true" selected={question.published}>Published</option>
                                        <option value="false" selected={!question.published}>Draft</option>
                                    </select>
                                    <div class="flex gap-2 mt-2">
                                        <button class="btn btn-success btn-sm" type="submit"
                                            ><span class="icon-[lucide--save] size-4"></span> Save</button>
                                        <button
                                            class="btn btn-error btn-sm"
                                            type="button"
                                            onclick={() => {
                                                editingQuestionId = null;
                                            }}>Cancel</button>
                                    </div>
                                </div>
                            </form>
                        {:else}
                            <div class="flex items-start justify-between gap-2">
                                <div>
                                    <div class="edit-card-field-value">{question.text}</div>
                                    <div class="edit-card-field-name">
                                        <div class="flex items-center gap-2">
                                            {#if question.published}
                                                <span class="badge badge-success badge-sm">Published</span>
                                            {:else}
                                                <span class="badge badge-warning badge-sm">Draft</span>
                                            {/if}
                                            <span class="badge badge-info badge-sm">{question.order}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex gap-2 shrink-0">
                                    <button
                                        class="btn btn-ghost btn-sm"
                                        type="button"
                                        onclick={() => {
                                            editingQuestionId = question.id;
                                        }}><span class="icon-[lucide--pencil] size-4"></span></button>
                                    <form method="POST" action="?/deleteQuestion" use:enhance>
                                        <input type="hidden" name="questionId" value={question.id} />
                                        <button
                                            class="btn btn-ghost btn-sm text-error"
                                            type="submit"
                                            onclick={(e) => {
                                                if (!confirm("Delete this question?")) e.preventDefault();
                                            }}><span class="icon-[lucide--trash-2] size-4"></span></button>
                                    </form>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
            {#if yesNoQuestions.length === 0}
                <div class="config-card-field-value">No Yes/No questions configured.</div>
            {/if}
            <details class="collapse collapse-arrow bg-base-100 border border-base-300">
                <summary class="collapse-title font-medium text-sm"
                    ><span class="icon-[lucide--plus] size-4 inline-block mr-1"></span>Add Yes/No Question</summary>
                <div class="collapse-content">
                    <form method="POST" action="?/createQuestion" use:enhance class="flex flex-col gap-2 pt-2">
                        <input type="hidden" name="questionType" value="yes_no" />
                        <label class="edit-card-field-name" for="new_yes_no_text">Question Text</label>
                        <input
                            id="new_yes_no_text"
                            class="edit-card-field-input w-full"
                            type="text"
                            name="text"
                            placeholder="Enter question text"
                            required />
                        <label class="edit-card-field-name" for="new_yes_no_order">Order</label>
                        <input
                            id="new_yes_no_order"
                            class="edit-card-field-input w-24"
                            type="number"
                            name="order"
                            value={yesNoQuestions.length}
                            min="0" />
                        <label class="edit-card-field-name" for="new_yes_no_published">Status</label>
                        <select id="new_yes_no_published" class="edit-card-field-input w-40" name="published">
                            <option value="false" selected>Draft</option>
                            <option value="true">Published</option>
                        </select>
                        <button class="btn btn-success btn-sm w-fit mt-2" type="submit"
                            ><span class="icon-[lucide--plus] size-4"></span> Add Question</button>
                    </form>
                </div>
            </details>
        </div>

        <div class="divider divider-accent">Multiple Choice</div>
        <div class="grid grid-cols-1 gap-4 mt-4">
            {#each multipleChoiceQuestions as question (question.id)}
                <div class="card bg-base-100 border border-base-300">
                    <div class="card-body p-4 gap-2">
                        {#if editingQuestionId === question.id}
                            <form
                                method="POST"
                                action="?/updateQuestion"
                                use:enhance={() => {
                                    return () => {
                                        editingQuestionId = null;
                                    };
                                }}>
                                <input type="hidden" name="questionId" value={question.id} />
                                <div class="flex flex-col gap-2">
                                    <label class="edit-card-field-name text-sm font-medium" for="mc_text_{question.id}"
                                        >Question Text</label>
                                    <input
                                        id="mc_text_{question.id}"
                                        class="edit-card-field-input input-bordered w-full"
                                        type="text"
                                        name="text"
                                        value={question.text}
                                        required />
                                    <label class="edit-card-field-name text-sm font-medium" for="mc_order_{question.id}"
                                        >Order</label>
                                    <input
                                        id="mc_order_{question.id}"
                                        class="edit-card-field-input input-bordered w-24"
                                        type="number"
                                        name="order"
                                        value={question.order}
                                        min="0" />
                                    <label
                                        class="edit-card-field-name text-sm font-medium"
                                        for="mc_published_{question.id}">Status</label>
                                    <select
                                        id="mc_published_{question.id}"
                                        class="select select-bordered w-40"
                                        name="published">
                                        <option value="true" selected={question.published}>Published</option>
                                        <option value="false" selected={!question.published}>Draft</option>
                                    </select>
                                    <div class="flex gap-2 mt-2">
                                        <button class="btn btn-primary btn-sm" type="submit"
                                            ><span class="icon-[lucide--save] size-4"></span> Save</button>
                                        <button
                                            class="btn btn-ghost btn-sm"
                                            type="button"
                                            onclick={() => {
                                                editingQuestionId = null;
                                            }}>Cancel</button>
                                    </div>
                                </div>
                            </form>
                        {:else}
                            <div class="flex items-start justify-between gap-2">
                                <div>
                                    <div class="config-card-field-value">{question.text}</div>
                                    <div class="config-card-field-name">
                                        <div class="edit-card-field-name">
                                            <div class="flex items-center gap-2">
                                                {#if question.published}
                                                    <span class="badge badge-success badge-sm">Published</span>
                                                {:else}
                                                    <span class="badge badge-warning badge-sm">Draft</span>
                                                {/if}
                                                <span class="badge badge-info badge-sm">{question.order}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex gap-2 shrink-0">
                                    <button
                                        class="btn btn-ghost btn-sm"
                                        type="button"
                                        onclick={() => {
                                            editingQuestionId = question.id;
                                        }}><span class="icon-[lucide--pencil] size-4"></span></button>
                                    <form method="POST" action="?/deleteQuestion" use:enhance>
                                        <input type="hidden" name="questionId" value={question.id} />
                                        <button
                                            class="btn btn-ghost btn-sm text-error"
                                            type="submit"
                                            onclick={(e) => {
                                                if (!confirm("Delete this question and all its choices?"))
                                                    e.preventDefault();
                                            }}><span class="icon-[lucide--trash-2] size-4"></span></button>
                                    </form>
                                </div>
                            </div>
                        {/if}

                        <div class="mt-3 border-t border-base-300 pt-3">
                            <div class="text-sm font-medium mb-2">Choices</div>
                            <div class="flex flex-col gap-2">
                                {#each question.choices as choice (choice.id)}
                                    <div class="flex items-center gap-2">
                                        {#if editingChoiceId === choice.id}
                                            <form
                                                method="POST"
                                                action="?/updateChoice"
                                                use:enhance={() => {
                                                    return () => {
                                                        editingChoiceId = null;
                                                    };
                                                }}
                                                class="flex items-center gap-2 flex-1">
                                                <input type="hidden" name="choiceId" value={choice.id} />
                                                <input
                                                    class="edit-card-field-input input-bordered input-sm flex-1"
                                                    type="text"
                                                    name="choiceText"
                                                    value={choice.choiceText}
                                                    required />
                                                <button class="btn btn-primary btn-sm" type="submit"
                                                    ><span class="icon-[lucide--save] size-4"></span></button>
                                                <button
                                                    class="btn btn-ghost btn-sm"
                                                    type="button"
                                                    onclick={() => {
                                                        editingChoiceId = null;
                                                    }}><span class="icon-[lucide--x] size-4"></span></button>
                                            </form>
                                        {:else}
                                            <span class="flex-1 text-sm">{choice.choiceText}</span>
                                            <button
                                                class="btn btn-ghost btn-xs"
                                                type="button"
                                                onclick={() => {
                                                    editingChoiceId = choice.id;
                                                }}><span class="icon-[lucide--pencil] size-3"></span></button>
                                            <form method="POST" action="?/deleteChoice" use:enhance>
                                                <input type="hidden" name="choiceId" value={choice.id} />
                                                <button
                                                    class="btn btn-ghost btn-xs text-error"
                                                    type="submit"
                                                    onclick={(e) => {
                                                        if (!confirm("Delete this choice?")) e.preventDefault();
                                                    }}><span class="icon-[lucide--trash-2] size-3"></span></button>
                                            </form>
                                        {/if}
                                    </div>
                                {/each}
                                {#if question.choices.length === 0}
                                    <div class="text-sm text-base-content/50">No choices yet.</div>
                                {/if}
                                <form
                                    method="POST"
                                    action="?/createChoice"
                                    use:enhance
                                    class="flex items-center gap-2 mt-1">
                                    <input type="hidden" name="questionId" value={question.id} />
                                    <input
                                        class="edit-card-field-input input-bordered input-sm flex-1"
                                        type="text"
                                        name="choiceText"
                                        placeholder="New choice text"
                                        required />
                                    <button class="btn btn-outline btn-sm" type="submit"
                                        ><span class="icon-[lucide--plus] size-4"></span> Add</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            {/each}
            {#if multipleChoiceQuestions.length === 0}
                <div class="config-card-field-value">No Multiple Choice questions configured.</div>
            {/if}
            <details class="collapse collapse-arrow bg-base-100 border border-base-300">
                <summary class="collapse-title font-medium text-sm"
                    ><span class="icon-[lucide--plus] size-4 inline-block mr-1"></span>Add Multiple Choice Question</summary>
                <div class="collapse-content">
                    <form method="POST" action="?/createQuestion" use:enhance class="flex flex-col gap-2 pt-2">
                        <input type="hidden" name="questionType" value="multiple_choice" />
                        <label class="edit-card-field-name text-sm font-medium" for="new_mc_text">Question Text</label>
                        <input
                            id="new_mc_text"
                            class="edit-card-field-input input-bordered w-full"
                            type="text"
                            name="text"
                            placeholder="Enter question text"
                            required />
                        <label class="edit-card-field-name text-sm font-medium" for="new_mc_order">Order</label>
                        <input
                            id="new_mc_order"
                            class="edit-card-field-input input-bordered w-24"
                            type="number"
                            name="order"
                            value={multipleChoiceQuestions.length}
                            min="0" />
                        <label class="edit-card-field-name text-sm font-medium" for="new_mc_published">Status</label>
                        <select id="new_mc_published" class="select select-bordered w-40" name="published">
                            <option value="false" selected>Draft</option>
                            <option value="true">Published</option>
                        </select>
                        <button class="btn btn-primary btn-sm w-fit mt-2" type="submit"
                            ><span class="icon-[lucide--plus] size-4"></span> Add Question</button>
                    </form>
                </div>
            </details>
        </div>

        <div class="divider divider-accent">Text Response</div>
        <div class="grid grid-cols-1 gap-4 mt-4">
            {#each textQuestions as question (question.id)}
                <div class="card bg-base-100 border border-base-300">
                    <div class="card-body p-4 gap-2">
                        {#if editingQuestionId === question.id}
                            <form
                                method="POST"
                                action="?/updateQuestion"
                                use:enhance={() => {
                                    return () => {
                                        editingQuestionId = null;
                                    };
                                }}>
                                <input type="hidden" name="questionId" value={question.id} />
                                <div class="flex flex-col gap-2">
                                    <label class="edit-card-field-name text-sm font-medium" for="txt_text_{question.id}"
                                        >Question Text</label>
                                    <input
                                        id="txt_text_{question.id}"
                                        class="edit-card-field-input input-bordered w-full"
                                        type="text"
                                        name="text"
                                        value={question.text}
                                        required />
                                    <label
                                        class="edit-card-field-name text-sm font-medium"
                                        for="txt_order_{question.id}">Order</label>
                                    <input
                                        id="txt_order_{question.id}"
                                        class="edit-card-field-input input-bordered w-24"
                                        type="number"
                                        name="order"
                                        value={question.order}
                                        min="0" />
                                    <label
                                        class="edit-card-field-name text-sm font-medium"
                                        for="txt_published_{question.id}">Status</label>
                                    <select
                                        id="txt_published_{question.id}"
                                        class="select select-bordered w-40"
                                        name="published">
                                        <option value="true" selected={question.published}>Published</option>
                                        <option value="false" selected={!question.published}>Draft</option>
                                    </select>
                                    <div class="flex gap-2 mt-2">
                                        <button class="btn btn-primary btn-sm" type="submit"
                                            ><span class="icon-[lucide--save] size-4"></span> Save</button>
                                        <button
                                            class="btn btn-ghost btn-sm"
                                            type="button"
                                            onclick={() => {
                                                editingQuestionId = null;
                                            }}>Cancel</button>
                                    </div>
                                </div>
                            </form>
                        {:else}
                            <div class="flex items-start justify-between gap-2">
                                <div>
                                    <div class="config-card-field-value">{question.text}</div>
                                    <div class="config-card-field-name">
                                        <div class="edit-card-field-name">
                                            <div class="flex items-center gap-2">
                                                {#if question.published}
                                                    <span class="badge badge-success badge-sm">Published</span>
                                                {:else}
                                                    <span class="badge badge-warning badge-sm">Draft</span>
                                                {/if}
                                                <span class="badge badge-info badge-sm">{question.order}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex gap-2 shrink-0">
                                    <button
                                        class="btn btn-ghost btn-sm"
                                        type="button"
                                        onclick={() => {
                                            editingQuestionId = question.id;
                                        }}><span class="icon-[lucide--pencil] size-4"></span></button>
                                    <form method="POST" action="?/deleteQuestion" use:enhance>
                                        <input type="hidden" name="questionId" value={question.id} />
                                        <button
                                            class="btn btn-ghost btn-sm text-error"
                                            type="submit"
                                            onclick={(e) => {
                                                if (!confirm("Delete this question?")) e.preventDefault();
                                            }}><span class="icon-[lucide--trash-2] size-4"></span></button>
                                    </form>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
            {#if textQuestions.length === 0}
                <div class="config-card-field-value">No Text Response questions configured.</div>
            {/if}
            <details class="collapse collapse-arrow bg-base-100 border border-base-300">
                <summary class="collapse-title font-medium text-sm"
                    ><span class="icon-[lucide--plus] size-4 inline-block mr-1"></span>Add Text Response Question</summary>
                <div class="collapse-content">
                    <form method="POST" action="?/createQuestion" use:enhance class="flex flex-col gap-2 pt-2">
                        <input type="hidden" name="questionType" value="text" />
                        <label class="edit-card-field-name text-sm font-medium" for="new_txt_text">Question Text</label>
                        <input
                            id="new_txt_text"
                            class="edit-card-field-input input-bordered w-full"
                            type="text"
                            name="text"
                            placeholder="Enter question text"
                            required />
                        <label class="edit-card-field-name text-sm font-medium" for="new_txt_order">Order</label>
                        <input
                            id="new_txt_order"
                            class="edit-card-field-input input-bordered w-24"
                            type="number"
                            name="order"
                            value={textQuestions.length}
                            min="0" />
                        <label class="edit-card-field-name text-sm font-medium" for="new_txt_published">Status</label>
                        <select id="new_txt_published" class="select select-bordered w-40" name="published">
                            <option value="false" selected>Draft</option>
                            <option value="true">Published</option>
                        </select>
                        <button class="btn btn-primary btn-sm w-fit mt-2" type="submit"
                            ><span class="icon-[lucide--plus] size-4"></span> Add Question</button>
                    </form>
                </div>
            </details>
        </div>
    </div>
</div>
