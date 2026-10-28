def calculate_budget(
    total_budget,
    travelers,
    days,
    daily_cost_per_person
):
    estimated_cost = (
        travelers * days * daily_cost_per_person
    )

    remaining_budget = total_budget - estimated_cost

    return {
        "estimated_cost": estimated_cost,
        "remaining_budget": remaining_budget,
        "is_within_budget": remaining_budget >= 0
    }


def allocate_budget(total_budget):
    return {
        "Transport": total_budget * 0.25,
        "Accommodation": total_budget * 0.30,
        "Food": total_budget * 0.20,
        "Activities": total_budget * 0.15,
        "Emergency": total_budget * 0.10
    }