<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';

    let journalEntry = '';
    let date;

    onMount(async () => {
        date = $page.params.date;  // get date from the URL

        const response = await fetch(`http://localhost:8001/journal/${date}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        journalEntry = data;
    });

    async function saveJournalEntry() {
        const response = await fetch(`http://localhost:8001/journal/${date}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: date,
                entry: journalEntry
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        goto('/');
    }
</script>

<div>
    <textarea bind:value={journalEntry}></textarea>
    <button on:click={saveJournalEntry}>Save</button>
    <button on:click={() => goto('/')}>Cancel</button>
</div>
