import csv


# Map for protocol numbers
protocol_map = {
    '1': 'icmp',
    '2': 'igmp',
    '6': 'tcp',
    '17': 'udp',
    '89': 'ospf',
    '132': 'sctp',
}


# Read the lookup table and store it in hashmap for quick lookup
def buildLookupTable(lookup_file):
    lookup_table = {}
    file_extension = lookup_file.split('.')[-1]

    if file_extension == 'txt':
        with open(lookup_file, mode='r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    dstport, protocol, tag = parts
                    lookup_table[(dstport, protocol)] = tag
    elif file_extension == 'csv':
        with open(lookup_file, 'r') as file:
            reader = csv.DictReader(file)
            # print("CSV Headers:", reader.fieldnames)
            for row in reader:
                dstport = row['dstport'].strip()
                protocol = row['protocol'].lower().strip()
                tag = row['tag'].strip()
                lookup_table[(dstport, protocol)] = tag
    else:
        print("File fomat not supported")
    return lookup_table


# Read the input flow log file and update the output maps accordingly for each line
def parse_file(flow_log_file, lookup_table):
    tag_counter = {}
    port_protocol = {}
    with open(flow_log_file, 'r') as file:
        for line in file:

            parts = line.strip().split()
            if not parts:  # Skip empty lines
                continue

            dstport = parts[6]
            protocol_number = parts[7]

            # Convert protocol number to text
            protocol_name = protocol_map.get(protocol_number, 'unknown')

            # Find the tag using (dstport, protocol_name) as the key
            tag = lookup_table.get((dstport, protocol_name), 'Untagged')
            print(f"Flow Log: {line.strip()} -> Tag: {tag}")
            
            # update tag_counter map
            tag_counter[tag]=tag_counter.get(tag,0)+1

            # update port_protocol map
            port_protocol[(dstport, protocol_name)]=port_protocol.get((dstport, protocol_name),0)+1

    return (tag_counter, port_protocol)


#  iterate through output maps for printing output.
def write_output(tag_counter, port_protocol_counter, output_file):
    with open(output_file, 'w') as f:
        # Write Tag Counts
        f.write("Tag Counts:\n")
        f.write("Tag,Count\n")
        for tag, count in tag_counter.items():
            f.write(f"{tag},{count}\n")

        # Write Port/Protocol Combination Counts
        f.write("\nPort/Protocol Combination Counts:\n")
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counter.items():
            f.write(f"{port},{protocol},{count}\n")

    print(f"Output written to {output_file}")


def main():
    lookup_file = 'lookup_file.txt'
    flow_log_file = 'log_file.txt'

    # Load the lookup table
    lookup_dict = buildLookupTable(lookup_file)

    # Parse the flow log file and map tags
    tag_counter, port_protocol_counter = parse_file(flow_log_file, lookup_dict)

    write_output(tag_counter,port_protocol_counter,"output.txt")

if __name__ == "__main__":
    main()


