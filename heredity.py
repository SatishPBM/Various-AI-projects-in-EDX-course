import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }


    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def num_of_genes(person, one_gene, two_genes):

    if person in one_gene:
        count = 1
    elif person in two_genes:
        count = 2
    else:
        count = 0

    return count


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    probability = 1
    
    for person in people:

        gene_count = num_of_genes(person, one_gene, two_genes)

        has_trait = False
        if person in have_trait:
            has_trait = True

        if people[person]["father"] is None and people[person]["mother"] is None:  ## if no parent info
            probability = probability * PROBS["gene"][gene_count] * PROBS["trait"][gene_count][has_trait]
        else:

            gene_count_mother = num_of_genes(people[person]["mother"], one_gene, two_genes)
            gene_count_father = num_of_genes(people[person]["father"], one_gene, two_genes)

            if gene_count == 0:

                if gene_count_mother == 0:
                    prob0_mother = 1 - PROBS["mutation"]
                elif gene_count_mother == 1:
                    prob0_mother = 0.5
                else:
                    prob0_mother = PROBS["mutation"]
                if gene_count_father == 0:
                    prob0_father = 1 - PROBS["mutation"]
                elif gene_count_father == 1:
                    prob0_father = 0.5
                else:
                    prob0_father = PROBS["mutation"]

                probability = probability * prob0_mother * prob0_father

            elif gene_count == 1:

                ### if coming from mother
                if gene_count_mother == 0:
                    prob1a_mother = PROBS["mutation"]
                elif gene_count_mother == 1:
                    prob1a_mother = 0.5
                else:
                    prob1a_mother = 1 - PROBS["mutation"]
                if gene_count_father == 0:
                    prob1a_father = 1 - PROBS["mutation"]
                elif gene_count_father == 1:
                    prob1a_father = 0.5
                else:
                    prob1a_father = PROBS["mutation"]

                ### if coming from father
                if gene_count_mother == 0:
                    prob1b_mother = 1 - PROBS["mutation"]
                elif gene_count_mother == 1:
                    prob1b_mother = 0.5
                else:
                    prob1b_mother = PROBS["mutation"]
                if gene_count_father == 0:
                    prob1b_father = PROBS["mutation"]
                elif gene_count_father == 1:
                    prob1b_father = 0.5
                else:
                    prob1b_father = 1 - PROBS["mutation"]

                probability = probability * ((prob1a_mother * prob1a_father) + (prob1b_mother * prob1b_father))
                
            else: ## gene count = 2

                if gene_count_mother == 0:
                    prob2_mother = PROBS["mutation"]
                elif gene_count_mother == 1:
                    prob2_mother = 0.5
                else:
                    prob2_mother = 1 - PROBS["mutation"]
                if gene_count_father == 0:
                    prob2_father = PROBS["mutation"]
                elif gene_count_father == 1:
                    prob2_father = 0.5
                else:
                    prob2_father = 1 - PROBS["mutation"] 
                
                probability = probability * prob2_mother * prob2_father

            probability = probability * PROBS["trait"][gene_count][has_trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:

        genes_count = num_of_genes(person, one_gene, two_genes)

        has_trait = False
        if person in have_trait:
            has_trait = True

        probabilities[person]["gene"][genes_count] = probabilities[person]["gene"][genes_count] + p
        probabilities[person]["trait"][has_trait] = probabilities[person]["trait"][has_trait] + p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        sum_trait = sum(probabilities[person]["trait"].values())
        sum_gene = sum(probabilities[person]["gene"].values())

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene] / sum_gene

        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] / sum_trait


if __name__ == "__main__":
    main()
