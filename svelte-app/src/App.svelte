<script>
    import dayjs from 'dayjs';
	import { onMount } from 'svelte';
	
	let preElement;
	let editable = true;
    let isDirty = false;
    let savedJournalEntry = '';
    
    let today = dayjs().format('YYYY-MM-DD');
    let journalEntry = '';
    let showJournal = false;

	async function getJournalEntry() {
        const response = await fetch(`http://localhost:8001/journal/2023-07-03`);
        const data = await response.json();
		journalEntry = data
        showJournal = true;
        savedJournalEntry = journalEntry;  // keep a copy of the fetched data
    }

	async function saveJournalEntry(entryText) {
        const response = await fetch(`http://localhost:8001/journal/2023-07-03`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({date: today, entry: entryText}),
        });
        const data = await response.json();
        isDirty = false;
    }

    async function updateEntry(e) {
        const currentEntry = document.querySelector('.journal-entry').textContent;
        if (isDirty) {
            if (confirm('This has been modified but not saved. Are you sure you want to exit without saving?')) {
                // await saveJournalEntry(currentEntry);
                // return to previous state
                journalEntry = savedJournalEntry;
                preElement.textContent = savedJournalEntry;

            } else {
                // if the user chooses to not exit, just return
                return;
            }
        }
        // assuming server responds with updated entry
        savedJournalEntry = currentEntry;
        isDirty = false;
    }

    function onInput(e) {
        isDirty = e.target.textContent !== savedJournalEntry;
    }

    onMount(() => {
        window.addEventListener('keyup', function(e) {
            if (e.key === 'Escape') {
                updateEntry(e);
            }
        });
    });

</script>
<div class="app-container">
    <main>

        <!-- here we need to fetch all the notes
        now display a calendar. 
        so we need to create our own calendar
        
        upon loading highlight today's date
        display the current month, so from the date module we can display all the dates
        -->

        <button class="date-container" on:click={getJournalEntry}>
            <p>{today}</p>
        </button>
        
        {#if showJournal}
            <div class="journal-container">
                <pre bind:this={preElement}
                class="journal-entry"
                contenteditable={editable}
                on:input={onInput}>{@html journalEntry}
                </pre>
                <button on:click={() => saveJournalEntry(document.querySelector('.journal-entry').textContent)}>Save</button>
            </div>  
        {/if}
    </main>
</div>

<!-- Your CSS here -->
<style>
    .app-container {
        background-color: #282828;
        height: 100vh;
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
    }

    main {
        text-align: center;
    }

    .date-container {
        border: 1px solid black;
        display: inline-block;
        padding: 1em;
        margin-bottom: 1em;
		background-color: aliceblue;
		color: black;
    }

    .date-container:hover {
        background-color: red;
        color: white;
        cursor: pointer;
    }

    .journal-container {
        padding: 1em;
        display: inline-block;
    }

    .journal-entry {
        color: yellowgreen;
        padding: 1em;
        white-space: pre-wrap;
        text-align: left;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>
