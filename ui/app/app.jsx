import { AppShell, Navbar, Header, Title, Text } from "@mantine/core"


const Head = (props) => {
    return (
        <Header {...props}>
            <Text>Application header</Text>
        </Header>
    )
}

const Nav = (props) => {
    return (
        <Navbar {...props}>
            <Navbar.Section>Section 1</Navbar.Section>
            <Navbar.Section>Section 2</Navbar.Section>
        </Navbar>
    )
}


export function App() {
    return (
        <AppShell
            navbar={<Nav width={{ base: 300 }} padding="xs" />}
            header={<Head height={60} padding="xs" />}
            styles={theme => ({ main: { backgroundColor: theme.colors.gray[0] } })}
        >
            <Text>Hoi</Text>
        </AppShell>
    )
}

