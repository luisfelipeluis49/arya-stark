import { faker } from '@faker-js/faker';

export const generateClients = (numClients) => {
    const clients = [];
    for (let i = 0; i < numClients; i++) {
        const riskCategories = [
            'financial', 'operational', 'law', 'reputation', 'market', 'tech', 'socialAndEnvironment'
        ];

        const riskPoints = {};
        let totalScore = 0;
        riskCategories.forEach(category => {
            const impact = faker.number.int({ min: 1, max: 5 });
            const probability = faker.number.int({ min: 1, max: 5 });
            const weight = impact * probability;
            totalScore += weight;
            riskPoints[category] = {
                impact,
                probability,
                weight,
                analysis: {
                    title: faker.lorem.sentence(),
                    description: faker.lorem.paragraph(),
                    references: [faker.internet.url()],
                    score: weight
                }
            };
        });

        clients.push({
            id: faker.string.uuid(),
            company_document: faker.number.int().toString(), // Assuming this is meant to be a number converted to a string
            companyName: faker.company.name(),
            riskPoints: riskPoints,
            totalScore: totalScore,
            icon: '...', // Replace with actual SVG data or placeholder
            description: faker.lorem.sentence()
        });

        console.log(clients[clients.length - 1]); // Corrected way to access the last element
    }

    return clients;
};

export function getCachedClients() {
    let cachedClients = generateClients(10);

    return cachedClients;
};
