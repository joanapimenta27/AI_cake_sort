def merge_slices_between_plates(adjacent_plates, placed_plate):
    
    count = 0
    changes_made = True

    while changes_made:
        #print("================================================================")
        changes_made = False

        previous_lower_diversity_best = None 
        while True:  # Handle lower diversity neighbors
            placed_plate_diversity = placed_plate.get_number_of_distinct_flavors()
            lower_diversity_neighbors = []

            for neighbor in adjacent_plates:
                neighbor_diversity = neighbor.get_number_of_distinct_flavors()
                if neighbor_diversity < placed_plate_diversity:
                    lower_diversity_neighbors.append(neighbor)
            #print(f"Lower diversity neighbors: {lower_diversity_neighbors}")
            best_neighbor = select_best_lower_diversity_neighbor(lower_diversity_neighbors, placed_plate)
            #print(f"Best lower diversity neighbor: {best_neighbor.composition() if best_neighbor else None}")
            if best_neighbor is None:
                #print("No best neighbor found in lower diversity.")
                break
            elif best_neighbor == previous_lower_diversity_best:
                count += 1
                #print(f"Count: {count}")
                if count > 3:
                    count = 0
                    #print("Best lower-diversity neighbor is the same as last iteration; skipping further trades.")
                    break
            else:
                previous_lower_diversity_best = best_neighbor
                target_flavor, _ = best_neighbor.get_dominant_flavor()
                pre_count = best_neighbor.number_of_slices()                
                deal_with_best_neighbor(best_neighbor, placed_plate, adjacent_plates)
                post_count = best_neighbor.number_of_slices()
                if post_count != pre_count:
                    #print("changes made")
                    changes_made = True
                

        previous_same_diversity_best = None           
        while True: # Handle same diversity neighbors
            #print("Entering same diversity neighbors loop")
            same_diversity_neighbors = get_same_diversity_neighbors(adjacent_plates, placed_plate)
            shared_flavor_neighbors = get_neighbors_with_shared_flavors(same_diversity_neighbors, placed_plate)
            best_same_diversity_neighbor = select_best_same_diversity_neighbor(shared_flavor_neighbors, placed_plate)
            #print(f"Best same diversity neighbor: {best_same_diversity_neighbor.composition() if best_same_diversity_neighbor else None}")

            if best_same_diversity_neighbor is None:
                    #print("No best neighbor found in same diversity.")
                    break
            elif best_same_diversity_neighbor == previous_same_diversity_best:
                count += 1
                #print(f"Count: {count}")
                if count > 3:
                    count = 0
                    #print("Best same-diversity neighbor is the same as last iteration; skipping further trades.")
                    break
            else:
                previous_same_diversity_best = best_same_diversity_neighbor
                target_flavor, _ = best_same_diversity_neighbor.get_dominant_flavor()
                pre_count = placed_plate.get_flavor_count(target_flavor)
                
                deal_with_best_same_diversity_neighbor(best_same_diversity_neighbor, placed_plate, adjacent_plates)
                
                post_count = placed_plate.get_flavor_count(target_flavor)
                if post_count != pre_count:
                    changes_made = True


        previous_higher_diversity_best = None 
        while True: #Handle higher diversity neighbors
            higher_diversity_neighbors = get_higher_diversity_neighbors(adjacent_plates, placed_plate)
            best_higher_diversity_neighbor = select_best_higher_diversity_neighbor(higher_diversity_neighbors, placed_plate)
            if best_higher_diversity_neighbor is None:
                #print("No best neighbor found in higher diversity.")
                break
            elif best_higher_diversity_neighbor == previous_higher_diversity_best:
                count += 1
                if count > 3:
                    count = 0
                    #print("Best same-diversity neighbor is the same as last iteration; skipping further trades.")
                    break
            else:
                previous_higher_diversity_best = best_higher_diversity_neighbor
                pre_count = best_higher_diversity_neighbor.number_of_slices()
                deal_with_best_higher_diversity_neighbor(best_higher_diversity_neighbor, placed_plate)
                post_count = best_higher_diversity_neighbor.number_of_slices()
                if post_count != pre_count:
                    #print("changes made")
                    changes_made = True



def deal_with_best_higher_diversity_neighbor(best_neighbor, placed_plate):
    #print(f"Dealing with best higher diversity neighbor: {best_neighbor}")
    placed_flavors = {s.cake_index() for s in placed_plate.slices if s is not None}
    neighbor_flavors = {s.cake_index() for s in best_neighbor.slices if s is not None}
    shared_flavors = placed_flavors.intersection(neighbor_flavors)
    #print(f"Shared flavors: {shared_flavors}")
    
    best_flavor = None
    max_diff = -float('inf')
    
    for flavor in shared_flavors:
        placed_count = placed_plate.get_flavor_count(flavor)
        neighbor_count = best_neighbor.get_flavor_count(flavor)
        diff = placed_count - neighbor_count
        if diff >= max_diff:
            max_diff = diff
            best_flavor = flavor
            #print(f"Best flavor: {best_flavor}")
            
    if best_flavor is not None:
        needed = placed_plate.max_slices - placed_plate.number_of_slices()
        max_give = best_neighbor.get_flavor_count(best_flavor)
        quantity_to_transfer = min(max_give, needed)
        #print(f"Needed: {needed}, Quantity to transfer: {quantity_to_transfer}")
        if quantity_to_transfer > 0:
            transferred = transfer_slices(best_neighbor, placed_plate, best_flavor, quantity_to_transfer)
            #print(f"Transferred {transferred} slices of flavor {best_flavor} from placed_plate to best_neighbor.")


def get_higher_diversity_neighbors(adjacent_plates, placed_plate):
    placed_diversity = placed_plate.get_number_of_distinct_flavors()
    higher_diversity_neighbors = []
    
    for neighbor in adjacent_plates:
        if neighbor.get_number_of_distinct_flavors() > placed_diversity:
            higher_diversity_neighbors.append(neighbor)
    
    return higher_diversity_neighbors


def select_best_higher_diversity_neighbor(higher_diversity_neighbors, placed_plate):
    best = None
    best_metric = -float('inf')
    best_neighbor_count = float('inf')
    
    placed_flavors = {s.cake_index() for s in placed_plate.slices if s is not None}
    
    for neighbor in higher_diversity_neighbors:
        neighbor_flavors = {s.cake_index() for s in neighbor.slices if s is not None}
        shared = placed_flavors.intersection(neighbor_flavors)
        for flavor in shared:
            placed_count = placed_plate.get_flavor_count(flavor)
            neighbor_count = neighbor.get_flavor_count(flavor)
            metric = placed_count - neighbor_count
            if (metric > best_metric) or (metric == best_metric and neighbor_count < best_neighbor_count):
                best = neighbor
                best_metric = metric
                best_neighbor_count = neighbor_count
    return best

def deal_with_best_same_diversity_neighbor(best_neighbor, placed_plate, adjacent_plates):
    target_flavor, _ = best_neighbor.get_dominant_flavor()
    #print("target flavor : ", target_flavor)
    needed = min(best_neighbor.max_slices - best_neighbor.get_flavor_count(target_flavor), best_neighbor.max_slices - best_neighbor.number_of_slices())
    available_in_placed = placed_plate.get_flavor_count(target_flavor)

    if available_in_placed < needed:
        other_neighbors = [n for n in adjacent_plates if n != best_neighbor]
        other_neighbors_sorted = sorted(other_neighbors, key=lambda p: (-p.get_number_of_distinct_flavors(), p.number_of_slices()))
        for neighbor in other_neighbors_sorted:
            neighbor_available = neighbor.get_flavor_count(target_flavor)
            if neighbor_available > 0:
                quantity_needed = needed - placed_plate.get_flavor_count(target_flavor)
                if quantity_needed <= 0:
                    break
                transfer_slices(neighbor, placed_plate, target_flavor, quantity_needed)
                available_in_placed = placed_plate.get_flavor_count(target_flavor)
                if available_in_placed >= needed:
                    break
    
    available_in_placed = placed_plate.get_flavor_count(target_flavor)
    quantity_to_transfer = min(needed, available_in_placed)
    if quantity_to_transfer > 0 and placed_plate.get_number_of_distinct_flavors() == 1:
        transfer_slices(best_neighbor, placed_plate, target_flavor, quantity_to_transfer)
    elif quantity_to_transfer > 0:
        transfer_slices(placed_plate, best_neighbor, target_flavor, quantity_to_transfer)
    
    compute_flavor_counts(best_neighbor)
    compute_flavor_counts(placed_plate)
    sorted_flavors = sorted(best_neighbor.flavour_counts.items(), key=lambda x: x[1], reverse=True)
    for flavor, count in sorted_flavors[1:]:
        if count > 0:
            if placed_plate.get_flavor_count(flavor) > 0:
                available_space = placed_plate.max_slices - placed_plate.number_of_slices()
                quantity_to_take = min(count, available_space)
                transfer_slices(best_neighbor, placed_plate, flavor, quantity_to_take)
                break

def select_best_same_diversity_neighbor(shared_neighbors, placed_plate):
    best_neighbor = None
    best_diff = -float('inf')
    
    placed_flavors = {s.cake_index() for s in placed_plate.slices if s is not None}
    
    for flavor in placed_flavors:
        placed_count = placed_plate.get_flavor_count(flavor)
        for neighbor in shared_neighbors:
            neighbor_count = neighbor.get_flavor_count(flavor)
            diff = neighbor_count - placed_count
            if diff > best_diff:
                best_diff = diff
                best_neighbor = neighbor
    
    return best_neighbor

def get_same_diversity_neighbors(adjacent_plates, placed_plate):
    placed_diversity = placed_plate.get_number_of_distinct_flavors()
    same_diversity_neighbors = []
    
    for neighbor in adjacent_plates:
        neighbor_diversity = neighbor.get_number_of_distinct_flavors()
        if neighbor_diversity == placed_diversity:
            same_diversity_neighbors.append(neighbor)
    
    return same_diversity_neighbors

def get_neighbors_with_shared_flavors(neighbors, placed_plate):
    placed_flavors = {s.cake_index() for s in placed_plate.slices if s is not None}
    shared_neighbors = []
    
    for neighbor in neighbors:
        neighbor_flavors = {s.cake_index() for s in neighbor.slices if s is not None}
        shared = placed_flavors.intersection(neighbor_flavors)
        if shared:
            shared_neighbors.append((neighbor, len(shared)))
    
    shared_neighbors.sort(key=lambda x: x[1], reverse=True)
    
    return [neighbor for neighbor, _ in shared_neighbors]

def compute_flavor_counts(plate):
    counts = {}
    for s in plate.slices:
        if s is not None:
            flavor = s.cake_index()
            counts[flavor] = counts.get(flavor, 0) + 1
    plate.flavour_counts = counts

def select_best_lower_diversity_neighbor(neighbors, placed_plate):
    best = None
    best_diversity = float('inf')
    best_count = 0

    for neighbor in neighbors:
        diversity = neighbor.get_number_of_distinct_flavors()
        if not neighbor.is_empty() and not neighbor.is_full():
            dominant_flavor, count = neighbor.get_dominant_flavor()
            if placed_plate.get_flavor_count(dominant_flavor) > 0:
                if diversity < best_diversity:
                    best = neighbor
                    best_diversity = diversity
                    best_count = count
                elif diversity == best_diversity and count > best_count:
                    best = neighbor
                    best_count = count

    return best

def deal_with_best_neighbor(best_neighbor, placed_plate, adjacent_plates):
    #print("Placed plate content: ", placed_plate.composition())
    target_flavor, _= best_neighbor.get_dominant_flavor()
    needed = min(best_neighbor.max_slices - best_neighbor.get_flavor_count(target_flavor), best_neighbor.max_slices - best_neighbor.number_of_slices())
    #print(f"Needed: {needed}")
    available_in_placed = placed_plate.get_flavor_count(target_flavor)
    if available_in_placed < needed:
        other_neighbors = [n for n in adjacent_plates if n != best_neighbor]
        other_neighbors_sorted = sorted(other_neighbors, key=lambda p: (-p.get_number_of_distinct_flavors(), p.number_of_slices()))

        for neighbor in other_neighbors_sorted:
            neighbor_available = neighbor.get_flavor_count(target_flavor)
            if neighbor_available > 0:
                quantity_needed = needed - placed_plate.get_flavor_count(target_flavor)
                if quantity_needed <= 0:
                    break
                #print(f"Transferring {quantity_needed} slices of flavor {target_flavor} from neighbor {neighbor}.")
                transferred = transfer_slices(neighbor, placed_plate, target_flavor, quantity_needed)
                #print(f"Gathered {transferred} slices of flavor {target_flavor} from neighbor {neighbor} to placed_plate.")
                available_in_placed = placed_plate.get_flavor_count(target_flavor)
                if available_in_placed >= needed:
                    break
    available_in_placed = placed_plate.get_flavor_count(target_flavor)
    quantity_to_transfer = min(needed, available_in_placed)
    if quantity_to_transfer > 0:
        #print(f"Placed plate flavor count: {placed_plate.get_flavor_count(target_flavor)}")
        transferred = transfer_slices(placed_plate, best_neighbor, target_flavor, quantity_to_transfer)
        #print(f"Transferred {transferred} slices of flavor {target_flavor} from placed_plate to best_neighbor.")
        #print(f"Placed plate flavor count: {placed_plate.get_flavor_count(target_flavor)}")



def transfer_slices(source_plate, target_plate, flavor, quantity):
    moved = 0
    for i, s in enumerate(source_plate.slices[:]):
        if moved >= quantity:
            break
        if s is not None and s.cake_index() == flavor:
            if not target_plate.is_full():
                if target_plate.add_slice(s):
                    source_plate.remove_slice(i)
                    moved += 1
            else:
                #print("Target plate is full, cannot transfer more slices.", target_plate.composition())
                break
    if moved > 0:
        compute_flavor_counts(source_plate)
        compute_flavor_counts(target_plate)
        #print("source plate flavour counts: ", source_plate.composition())
        #print("target plate flavor counts: ", target_plate.composition())
    return moved