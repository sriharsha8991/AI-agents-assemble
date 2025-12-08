from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    job_title: Optional[str] = Field(
        default=None,
        description="Job title or role, e.g. 'Senior Software Engineer'.",
    )
    company: Optional[str] = Field(
        default=None,
        description="Company or organization name.",
    )
    location: Optional[str] = Field(
        default=None,
        description="Location of the role, if mentioned.",
    )
    start_date: Optional[str] = Field(
        default=None,
        description="Start date in free-text (e.g. 'Jan 2020') as found in the resume.",
    )
    end_date: Optional[str] = Field(
        default=None,
        description="End date in free-text (e.g. 'Present', 'Jun 2024').",
    )
    responsibilities: List[str] = Field(
        default_factory=list,
        description="Bullet points or sentences describing responsibilities and achievements.",
    )


class EducationItem(BaseModel):
    degree: Optional[str] = Field(
        default=None,
        description="Degree name, e.g. 'B.Sc. Computer Science'.",
    )
    institution: Optional[str] = Field(
        default=None,
        description="Name of the university or institution.",
    )
    location: Optional[str] = Field(
        default=None,
        description="Location of the institution, if available.",
    )
    start_date: Optional[str] = Field(
        default=None,
        description="Start date in free-text as found in the resume.",
    )
    end_date: Optional[str] = Field(
        default=None,
        description="End date or graduation date in free-text.",
    )
    grade: Optional[str] = Field(
        default=None,
        description="GPA, grade, or classification if mentioned.",
    )


class CertificationItem(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Certification or course name.",
    )
    issuer: Optional[str] = Field(
        default=None,
        description="Issuing organization.",
    )
    date: Optional[str] = Field(
        default=None,
        description="Date or year obtained (free-text).",
    )


class ContactInfo(BaseModel):
    email: Optional[str] = Field(
        default=None,
        description="Primary email address of the candidate.",
    )
    phone: Optional[str] = Field(
        default=None,
        description="Primary phone number of the candidate in free-text.",
    )
    location: Optional[str] = Field(
        default=None,
        description="Location or address line(s) as described in the resume.",
    )
    linkedin: Optional[str] = Field(
        default=None,
        description="LinkedIn profile URL, if present.",
    )
    github: Optional[str] = Field(
        default=None,
        description="GitHub profile URL, if present.",
    )
    website: Optional[str] = Field(
        default=None,
        description="Personal website or portfolio URL, if present.",
    )


class Resume(BaseModel):
    full_name: Optional[str] = Field(
        default=None,
        description="Full name of the candidate.",
    )
    contact: Optional[ContactInfo] = Field(
        default=None,
        description="Contact information extracted from the resume.",
    )
    summary: Optional[str] = Field(
        default=None,
        description="Professional summary, objective, or headline from the resume.",
    )
    experience: List[ExperienceItem] = Field(
        default_factory=list,
        description="Ordered list of work experience entries, most recent first if clear.",
    )
    education: List[EducationItem] = Field(
        default_factory=list,
        description="Academic history, degrees, and institutions.",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of key skills, technologies, tools, and competencies.",
    )
    certifications: List[CertificationItem] = Field(
        default_factory=list,
        description="Professional certifications, licenses, and relevant courses.",
    )
    languages: List[str] = Field(
        default_factory=list,
        description="Languages spoken, optionally with proficiency if present.",
    )
    raw_text: Optional[str] = Field(
        default=None,
        description="Optional raw or lightly cleaned text of the resume if the model chooses to include it.",
    )
