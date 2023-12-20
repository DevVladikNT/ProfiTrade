import { Card, Flex, Title, TextInput, Button } from "@tremor/react";

function SearchBar() {
    return (
        <Card className="mb-4 mt-4">
            <Title>Company:</Title>
            <Flex flexDirection="row">
                <TextInput placeholder="Name / Ticker / Figi"/>
                <Button className="ml-5">Search</Button>
            </Flex>
        </Card>
    );
}

export default SearchBar;