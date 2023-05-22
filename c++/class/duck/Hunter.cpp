//
// Created by Shrekulka on 13.05.2023.
//

#include "Hunter.h"

#include <utility>

Hunter::Hunter() : m_nameHunter("Kuzya")
{
}

Hunter::Hunter(const string &name) : m_nameHunter(name)
{
}

Hunter::Hunter(const Hunter& other) : m_nameHunter(other.m_nameHunter)
{
}

void Hunter::CShow() const
{
	cout << "I am a drunken hunter " << m_nameHunter << " !!!\n" << '\n';
}

Hunter::~Hunter()
{
}