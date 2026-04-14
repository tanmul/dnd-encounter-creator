const BASE_URL = 'http://localhost:8000';

export const api = {
  /**
   * GET /monsters
   * Retrieves the full list (or a subset) of monsters for the manual selection table.
   */
  async getAllMonsters() {
    try {
      const response = await fetch(`${BASE_URL}/monsters`);
      if (!response.ok) throw new Error('Failed to fetch monsters');
      return await response.json();
    } catch (error) {
      console.error("API Error (getAllMonsters):", error);
      throw error;
    }
  },

  /**
   * POST /generate-encounter
   * Sends the EncounterRequest (Player info + Filters) to the backend.
   * @param {Object} encounterData - Matches the Pydantic EncounterRequest model.
   */
  async generateEncounter(encounterData) {
    try {
      const response = await fetch(`${BASE_URL}/generate-encounter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(encounterData),
      });

      if (!response.ok) {
        // This helps catch Pydantic validation errors (422 Unprocessable Entity)
        const errorData = await response.json();
        console.error("Validation Error:", errorData);
        throw new Error('Failed to generate encounter');
      }

      return await response.json();
    } catch (error) {
      console.error("API Error (generateEncounter):", error);
      throw error;
    }
  }
};